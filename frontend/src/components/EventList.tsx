import type { EventRead } from '@api/events'
import { formatDateRange } from '@utils/datetime'

interface EventListProps {
  events: EventRead[]
  loading: boolean
  error: unknown
}

const formatStatusLabel = (status: EventRead['status']): string =>
  status.charAt(0).toUpperCase() + status.slice(1)

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
            <p className={`status-badge status-${event.status}`}>
              {formatStatusLabel(event.status)}
            </p>
            <h3>{event.title}</h3>
            <p className="muted">{formatDateRange(event.starts_at, event.ends_at)}</p>
          </header>
          {event.description && <p className="event-description">{event.description}</p>}
          <dl className="event-meta">
            <div>
              <dt>Sport</dt>
              <dd className="mono">{event.sport_id}</dd>
            </div>
            {event.venue_id && (
              <div>
                <dt>Venue</dt>
                <dd className="mono">{event.venue_id}</dd>
              </div>
            )}
            {event.ticket_url && (
              <div>
                <dt>Tickets</dt>
                <dd>
                  <a href={event.ticket_url} target="_blank" rel="noreferrer">
                    Buy tickets ↗
                  </a>
                </dd>
              </div>
            )}
          </dl>
          <section className="participants">
            <h4>Participants</h4>
            {event.participants && event.participants.length > 0 ? (
              <ul>
                {event.participants.map((participant) => (
                  <li key={`${participant.team_id}-${participant.role}`}>
                    <span className={`role-chip role-${participant.role}`}>{participant.role}</span>
                    <span className="mono">{participant.team_id}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="muted">Participants will be announced soon.</p>
            )}
          </section>
        </article>
      ))}
    </section>
  )
}

export default EventList
