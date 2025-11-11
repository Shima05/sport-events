import { render, screen } from '@testing-library/react'

import type { EventRead } from '@api/events'

import { EventList } from './EventList'

const buildEvent = (overrides: Partial<EventRead> = {}): EventRead => ({
  id: '1',
  sport_id: 'sport-1',
  sport_name: 'Soccer',
  venue_id: null,
  title: 'Sample Event',
  description: 'Details to follow',
  starts_at: new Date('2025-01-01T10:00:00Z').toISOString(),
  ends_at: new Date('2025-01-01T12:00:00Z').toISOString(),
  status: 'scheduled',
  ticket_url: null,
  participants: [
    { team_id: 'team-home', role: 'home', team_name: 'Salzburg' },
    { team_id: 'team-away', role: 'away', team_name: 'Sturm' },
  ],
  ...overrides,
})

describe('EventList', () => {
  it('renders events with meta information', () => {
    const events = [buildEvent()]

    render(<EventList events={events} loading={false} error={null} />)

    const headline = screen.getByRole('heading', { name: /salzburg vs\. sturm/i })
    expect(headline.textContent).toContain('Wed., 01.01.2025, 10:00')
    expect(headline.textContent).toContain('Soccer')
  })

  it('renders empty state', () => {
    render(<EventList events={[]} loading={false} error={null} />)

    expect(screen.getByText(/no events found/i)).toBeInTheDocument()
  })
})
