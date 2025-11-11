import type { EventRead } from '@api/events'

interface EventListProps {
  events: EventRead[]
  loading: boolean
  error: unknown
}

const formatStatusLabel = (status: EventRead['status']): string =>
  status.charAt(0).toUpperCase() + status.slice(1)

const formatDateSummary = (iso: string): string => {
  const date = new Date(iso)
  const weekday = new Intl.DateTimeFormat('en-GB', {
    weekday: 'short',
    timeZone: 'UTC',
  }).format(date)
  const day = String(date.getUTCDate()).padStart(2, '0')
  const month = String(date.getUTCMonth() + 1).padStart(2, '0')
  const year = date.getUTCFullYear()
  const time = new Intl.DateTimeFormat('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
    timeZone: 'UTC',
  }).format(date)
  return `${weekday}., ${day}.${month}.${year}, ${time}`
}

const formatParticipantsLine = (participants: EventRead['participants']): string | null => {
  if (!participants?.length) {
    return null
  }
  const home = participants.find((p) => p.role === 'home')
  const away = participants.find((p) => p.role === 'away')
  if (!home || !away) {
    return null
  }
  const homeLabel = home.team_name ?? home.team_id
  const awayLabel = away.team_name ?? away.team_id
  return `${homeLabel} vs. ${awayLabel}`
}

const buildEventHeadline = (event: EventRead): string => {
  const datePart = formatDateSummary(event.starts_at)
  const sportLabel = event.sport_name ?? event.sport_id
  const duel = formatParticipantsLine(event.participants)
  const matchLabel = duel ?? event.title
  return `${datePart}, ${sportLabel}, ${matchLabel}`
}

export const EventList = ({ events, loading, error }: EventListProps): JSX.Element => {
  if (loading) {
    return (
      <section className="panel info">
        <p>Loading events…</p>
      </section>
    )
  }

  if (error) {
    const description = error instanceof Error ? error.message : 'Unable to reach the API.'
    return (
      <section className="panel error" role="alert">
        <p>We could not load the events.</p>
        <p className="muted">{description}</p>
      </section>
    )
  }

  if (!events.length) {
    return (
      <section className="panel empty">
        <p>No events found. Try adjusting your filters.</p>
      </section>
    )
  }

  return (
    <section className="event-grid">
      {events.map((event) => (
        <article key={event.id} className="event-card">
          <header>
            <div className="event-headline">
              <h3>{buildEventHeadline(event)}</h3>
              <span className={`status-pill status-${event.status}`}>
                {formatStatusLabel(event.status)}
              </span>
            </div>
          </header>
        </article>
      ))}
    </section>
  )
}

export default EventList
