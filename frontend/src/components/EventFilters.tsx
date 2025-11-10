import { useEffect, useState, type ChangeEvent, type FormEvent } from 'react'

import {
  ORDER_DIRECTIONS,
  defaultEventFilters,
  type EventStatus,
  type EventsQuery,
  type OrderDirection,
} from '@api/events'
import { fromDateTimeLocalInput, toDateTimeLocalInput } from '@utils/datetime'

const STATUS_OPTIONS: (EventStatus | 'all')[] = [
  'all',
  'scheduled',
  'live',
  'finished',
  'cancelled',
]
const PAGE_SIZE_OPTIONS = [10, 20, 50]

type FormState = {
  sport_id: string
  status: string
  date_from: string
  date_to: string
  order: OrderDirection
  page_size: string
}

const toFormState = (filters: EventsQuery): FormState => ({
  sport_id: filters.sport_id ?? '',
  status: filters.status ?? '',
  date_from: toDateTimeLocalInput(filters.date_from),
  date_to: toDateTimeLocalInput(filters.date_to),
  order: (filters.order ?? defaultEventFilters.order) as OrderDirection,
  page_size: String(filters.page_size ?? defaultEventFilters.page_size),
})

const toFilters = (state: FormState): EventsQuery => ({
  sport_id: state.sport_id.trim() || undefined,
  status: state.status && state.status !== 'all' ? (state.status as EventStatus) : undefined,
  date_from: fromDateTimeLocalInput(state.date_from),
  date_to: fromDateTimeLocalInput(state.date_to),
  order: state.order,
  page: 1,
  page_size: Number(state.page_size) || defaultEventFilters.page_size,
})

interface EventFiltersProps {
  filters: EventsQuery
  onApply: (next: EventsQuery) => void
  onReset: () => void
  disabled?: boolean
}

export const EventFilters = ({
  filters,
  onApply,
  onReset,
  disabled = false,
}: EventFiltersProps): JSX.Element => {
  const [formState, setFormState] = useState<FormState>(() => toFormState(filters))

  useEffect(() => {
    setFormState(toFormState(filters))
  }, [filters])

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = event.target
    setFormState((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    onApply(toFilters(formState))
  }

  const handleReset = () => {
    setFormState(toFormState(defaultEventFilters))
    onReset()
  }

  return (
    <section id="filters" className="panel">
      <form className="filters-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>
            <span>Sport ID</span>
            <input
              type="text"
              name="sport_id"
              value={formState.sport_id}
              onChange={handleChange}
              placeholder="UUID"
              disabled={disabled}
            />
          </label>

          <label>
            <span>Status</span>
            <select
              name="status"
              value={formState.status}
              onChange={handleChange}
              disabled={disabled}
            >
              {STATUS_OPTIONS.map((option) => (
                <option key={option} value={option === 'all' ? '' : option}>
                  {option === 'all' ? 'All' : option.charAt(0).toUpperCase() + option.slice(1)}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Starts After</span>
            <input
              type="datetime-local"
              name="date_from"
              value={formState.date_from}
              onChange={handleChange}
              disabled={disabled}
            />
          </label>

          <label>
            <span>Starts Before</span>
            <input
              type="datetime-local"
              name="date_to"
              value={formState.date_to}
              onChange={handleChange}
              disabled={disabled}
            />
          </label>

          <label>
            <span>Order</span>
            <select
              name="order"
              value={formState.order}
              onChange={handleChange}
              disabled={disabled}
            >
              {ORDER_DIRECTIONS.map((direction) => (
                <option key={direction} value={direction}>
                  {direction === 'asc' ? 'Earliest first' : 'Latest first'}
                </option>
              ))}
            </select>
          </label>

          <label>
            <span>Page size</span>
            <select
              name="page_size"
              value={formState.page_size}
              onChange={handleChange}
              disabled={disabled}
            >
              {PAGE_SIZE_OPTIONS.map((size) => (
                <option key={size} value={size}>
                  {size} per page
                </option>
              ))}
            </select>
          </label>
        </div>

        <div className="filters-actions">
          <button type="button" className="secondary" onClick={handleReset} disabled={disabled}>
            Reset
          </button>
          <button type="submit" className="primary" disabled={disabled}>
            Apply Filters
          </button>
        </div>
      </form>
    </section>
  )
}

export default EventFilters
