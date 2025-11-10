import { render, screen } from '@testing-library/react'

import type { EventRead } from '@api/events'

import { EventList } from './EventList'

const buildEvent = (overrides: Partial<EventRead> = {}): EventRead => ({
  id: '1',
  sport_id: 'sport-1',
  venue_id: null,
  title: 'Sample Event',
  description: 'Details to follow',
  starts_at: new Date('2025-01-01T10:00:00Z').toISOString(),
  ends_at: new Date('2025-01-01T12:00:00Z').toISOString(),
  status: 'scheduled',
  ticket_url: null,
  participants: [],
  ...overrides,
})

describe('EventList', () => {
  it('renders events with meta information', () => {
    const events = [buildEvent()]

    render(<EventList events={events} loading={false} error={null} />)

    expect(screen.getByText(/sample event/i)).toBeInTheDocument()
    expect(screen.getByText(/sport-1/i)).toBeInTheDocument()
  })

  it('renders empty state', () => {
    render(<EventList events={[]} loading={false} error={null} />)

    expect(screen.getByText(/no events found/i)).toBeInTheDocument()
  })
})
