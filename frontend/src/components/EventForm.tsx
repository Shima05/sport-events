import { useState, type ChangeEvent, type FormEvent } from 'react'

import { createEvent, type EventCreatePayload } from '@api/events'
import { fromDateTimeLocalInput } from '@utils/datetime'

const INITIAL_STATE = {
  sport_id: '',
  title: '',
  description: '',
  starts_at: '',
  ends_at: '',
}

interface EventFormProps {
  onCreated?: () => void | Promise<void>
}

export const EventForm = ({ onCreated }: EventFormProps): JSX.Element => {
  const [formState, setFormState] = useState(INITIAL_STATE)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target
    setFormState((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const startsAt = fromDateTimeLocalInput(formState.starts_at)
    const endsAt = fromDateTimeLocalInput(formState.ends_at)

    if (!formState.sport_id.trim()) {
      setError('Sport ID is required.')
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

    const payload: EventCreatePayload = {
      sport_id: formState.sport_id.trim(),
      venue_id: null,
      title: formState.title.trim(),
      description: formState.description.trim() || null,
      starts_at: startsAt,
      ends_at: endsAt,
      status: 'scheduled',
      ticket_url: null,
      participants: [],
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
          <h2>Add a new fixture</h2>
          <p className="muted">Enter the primary details below. You can always enrich it later.</p>
        </header>

        <label>
          <span>Sport ID *</span>
          <input
            type="text"
            name="sport_id"
            value={formState.sport_id}
            onChange={handleChange}
            placeholder="Sport UUID"
            disabled={submitting}
            required
          />
        </label>

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
