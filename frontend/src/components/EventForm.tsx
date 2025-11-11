import { useState, type ChangeEvent, type FormEvent } from 'react'

import { createEvent, type EventCreatePayload, type EventParticipantRole } from '@api/events'
import { useSports } from '@hooks/useSports'
import { useTeams } from '@hooks/useTeams'
import { fromDateTimeLocalInput } from '@utils/datetime'

const INITIAL_STATE = {
  sport_id: '',
  title: '',
  description: '',
  starts_at: '',
  ends_at: '',
  home_team_id: '',
  away_team_id: '',
}

interface EventFormProps {
  onCreated?: () => void | Promise<void>
}

export const EventForm = ({ onCreated }: EventFormProps): JSX.Element => {
  const [formState, setFormState] = useState(INITIAL_STATE)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const { sports, loading: sportsLoading, error: sportsError } = useSports()
  const hasSports = sports.length > 0
  const {
    teams,
    loading: teamsLoading,
    error: teamsError,
  } = useTeams(formState.sport_id || undefined)
  const hasTeamOptions = teams.length > 0

  const handleChange = (
    event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) => {
    const { name, value } = event.target
    setFormState((prev) => ({
      ...prev,
      [name]: value,
      ...(name === 'sport_id'
        ? {
            home_team_id: '',
            away_team_id: '',
          }
        : {}),
    }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const startsAt = fromDateTimeLocalInput(formState.starts_at)
    const endsAt = fromDateTimeLocalInput(formState.ends_at)

    if (!formState.sport_id.trim()) {
      setError('Sport is required.')
      return
    }
    if (!formState.title.trim()) {
      setError('Title is required.')
      return
    }
    if (!startsAt || !endsAt) {
      setError('Valid start and end dates are required.')
      return
    }

    const participants: EventCreatePayload['participants'] = []
    const appendParticipant = (teamId: string, role: EventParticipantRole) => {
      const trimmed = teamId.trim()
      if (trimmed) {
        participants.push({ team_id: trimmed, role })
      }
    }
    appendParticipant(formState.home_team_id, 'home')
    appendParticipant(formState.away_team_id, 'away')

    const payload: EventCreatePayload = {
      sport_id: formState.sport_id.trim(),
      venue_id: null,
      title: formState.title.trim(),
      description: formState.description.trim() || null,
      starts_at: startsAt,
      ends_at: endsAt,
      status: 'scheduled',
      ticket_url: null,
      participants,
    }

    setSubmitting(true)
    setError(null)
    setSuccess(null)
    try {
      await createEvent(payload)
      setSuccess('Event created successfully.')
      setFormState(INITIAL_STATE)
      setError(null)
      await onCreated?.()
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unable to create event.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="panel">
      <form className="event-form" onSubmit={handleSubmit} noValidate>
        <header>
          <p className="eyebrow">Create event</p>
          <h2>Add a new Event</h2>
          <p className="muted">Enter the primary details below.</p>
        </header>

        <label>
          <span>Sport *</span>
          {hasSports ? (
            <select
              name="sport_id"
              value={formState.sport_id}
              onChange={handleChange}
              disabled={submitting || sportsLoading}
              required
            >
              <option value="">Select a sport</option>
              {sports.map((sport) => (
                <option key={sport.id} value={sport.id}>
                  {sport.name}
                </option>
              ))}
            </select>
          ) : (
            <input
              type="text"
              name="sport_id"
              value={formState.sport_id}
              onChange={handleChange}
              placeholder="Sport UUID"
              disabled={submitting}
              required
            />
          )}
        </label>
        {!hasSports && !sportsLoading && (
          <p className="form-hint">No sports found. Enter the sport UUID manually.</p>
        )}
        {sportsError && (
          <p className="form-feedback error" role="alert">
            Unable to load sports list.
          </p>
        )}

        <section className="participants-panel">
          <h3>Participants</h3>
          {!formState.sport_id && <p className="form-hint">Select a sport to choose teams.</p>}
          {formState.sport_id && hasTeamOptions && (
            <div className="form-grid">
              <label>
                <span>Home team</span>
                <select
                  name="home_team_id"
                  value={formState.home_team_id}
                  onChange={handleChange}
                  disabled={teamsLoading || submitting}
                >
                  <option value="">Select home team</option>
                  {teams.map((team) => (
                    <option key={team.id} value={team.id}>
                      {team.name}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                <span>Away team</span>
                <select
                  name="away_team_id"
                  value={formState.away_team_id}
                  onChange={handleChange}
                  disabled={teamsLoading || submitting}
                >
                  <option value="">Select away team</option>
                  {teams.map((team) => (
                    <option key={team.id} value={team.id}>
                      {team.name}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          )}
          {formState.sport_id && !hasTeamOptions && !teamsLoading && (
            <div className="form-grid">
              <label>
                <span>Home team ID</span>
                <input
                  type="text"
                  name="home_team_id"
                  value={formState.home_team_id}
                  onChange={handleChange}
                  placeholder="Home team UUID"
                  disabled={submitting}
                />
              </label>
              <label>
                <span>Away team ID</span>
                <input
                  type="text"
                  name="away_team_id"
                  value={formState.away_team_id}
                  onChange={handleChange}
                  placeholder="Away team UUID"
                  disabled={submitting}
                />
              </label>
            </div>
          )}
          {teamsLoading && <p className="form-hint">Loading teams…</p>}
          {teamsError && (
            <p className="form-feedback error" role="alert">
              Unable to load teams for the selected sport.
            </p>
          )}
        </section>

        <label>
          <span>Title *</span>
          <input
            type="text"
            name="title"
            value={formState.title}
            onChange={handleChange}
            placeholder="e.g. Friendly Match"
            disabled={submitting}
            required
          />
        </label>

        <label>
          <span>Description</span>
          <textarea
            name="description"
            rows={3}
            value={formState.description}
            onChange={handleChange}
            placeholder="Optional notes..."
            disabled={submitting}
          />
        </label>

        <div className="form-grid">
          <label>
            <span>Starts at *</span>
            <input
              type="datetime-local"
              name="starts_at"
              value={formState.starts_at}
              onChange={handleChange}
              disabled={submitting}
              required
            />
          </label>

          <label>
            <span>Ends at *</span>
            <input
              type="datetime-local"
              name="ends_at"
              value={formState.ends_at}
              onChange={handleChange}
              disabled={submitting}
              required
            />
          </label>
        </div>

        {error && (
          <p className="form-feedback error" role="alert">
            {error}
          </p>
        )}
        {success && <p className="form-feedback success">{success}</p>}

        <div className="filters-actions">
          <button type="submit" className="primary" disabled={submitting}>
            {submitting ? 'Saving…' : 'Add event'}
          </button>
        </div>
      </form>
    </section>
  )
}

export default EventForm
