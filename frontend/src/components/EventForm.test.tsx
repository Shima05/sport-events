import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { createEvent } from '@api/events'
import { useSports } from '@hooks/useSports'
import { useTeams } from '@hooks/useTeams'

import { EventForm } from './EventForm'

vi.mock('@api/events', () => ({
  createEvent: vi.fn(),
}))

vi.mock('@hooks/useSports', () => ({
  useSports: vi.fn(),
}))

vi.mock('@hooks/useTeams', () => ({
  useTeams: vi.fn(),
}))

const mockedCreateEvent = createEvent as unknown as ReturnType<typeof vi.fn>
const mockedUseSports = useSports as unknown as ReturnType<typeof vi.fn>
const mockedUseTeams = useTeams as unknown as ReturnType<typeof vi.fn>

describe('EventForm', () => {
  beforeEach(() => {
    mockedCreateEvent.mockReset()
    mockedUseSports.mockReset()
    mockedUseTeams.mockReset()
    mockedUseSports.mockReturnValue({ sports: [], loading: false, error: null })
    mockedUseTeams.mockReturnValue({ teams: [], loading: false, error: null })
  })

  it('submits payload to the API and notifies parent', async () => {
    mockedCreateEvent.mockResolvedValue({})
    mockedUseSports.mockReturnValue({
      sports: [
        { id: 'sport-123', name: 'Soccer', code: 'soccer' },
        { id: 'sport-456', name: 'Basketball', code: 'basketball' },
      ],
      loading: false,
      error: null,
    })
    mockedUseTeams.mockReturnValue({
      teams: [
        { id: 'team-home', sport_id: 'sport-123', name: 'Salzburg', abbr: null },
        { id: 'team-away', sport_id: 'sport-123', name: 'Sturm', abbr: null },
      ],
      loading: false,
      error: null,
    })
    const onCreated = vi.fn()
    const user = userEvent.setup()

    render(<EventForm onCreated={onCreated} />)

    await user.selectOptions(screen.getByLabelText(/sport/i), 'sport-123')
    await user.selectOptions(screen.getByLabelText(/home team/i), 'team-home')
    await user.selectOptions(screen.getByLabelText(/away team/i), 'team-away')
    await user.type(screen.getByLabelText(/title/i), ' Test Match ')
    await user.type(screen.getByLabelText(/starts at/i), '2025-01-01T10:00')
    await user.type(screen.getByLabelText(/ends at/i), '2025-01-01T12:00')

    await user.click(screen.getByRole('button', { name: /add event/i }))

    await waitFor(() => {
      expect(mockedCreateEvent).toHaveBeenCalled()
    })

    const payload = mockedCreateEvent.mock.calls[0][0]
    expect(payload).toMatchObject({
      sport_id: 'sport-123',
      title: 'Test Match',
      description: null,
      participants: [
        { team_id: 'team-home', role: 'home' },
        { team_id: 'team-away', role: 'away' },
      ],
    })
    expect(onCreated).toHaveBeenCalled()
  })

  it('falls back to manual sport entry when no sports exist', async () => {
    mockedUseSports.mockReturnValue({ sports: [], loading: false, error: null })
    mockedUseTeams.mockReturnValue({ teams: [], loading: false, error: null })
    mockedCreateEvent.mockResolvedValue({})
    const user = userEvent.setup()

    render(<EventForm />)

    await user.type(screen.getByLabelText(/sport/i), 'abc-uuid')
    await user.type(screen.getByLabelText(/title/i), 'Quick Add')
    await user.type(screen.getByLabelText(/starts at/i), '2025-01-01T10:00')
    await user.type(screen.getByLabelText(/ends at/i), '2025-01-01T12:00')
    await user.click(screen.getByRole('button', { name: /add event/i }))

    await waitFor(() => expect(mockedCreateEvent).toHaveBeenCalled())
    expect(mockedCreateEvent.mock.calls[0][0].sport_id).toBe('abc-uuid')
  })

  it('shows validation error when fields are missing', async () => {
    const user = userEvent.setup()
    render(<EventForm />)

    await user.click(screen.getByRole('button', { name: /add event/i }))

    expect(screen.getByText(/sport is required/i)).toBeInTheDocument()
    expect(mockedCreateEvent).not.toHaveBeenCalled()
  })
})
