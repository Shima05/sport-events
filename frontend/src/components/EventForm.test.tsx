import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { createEvent } from '@api/events'

import { EventForm } from './EventForm'

vi.mock('@api/events', () => ({
  createEvent: vi.fn(),
}))

const mockedCreateEvent = createEvent as unknown as ReturnType<typeof vi.fn>

describe('EventForm', () => {
  beforeEach(() => {
    mockedCreateEvent.mockReset()
  })

  it('submits payload to the API and notifies parent', async () => {
    mockedCreateEvent.mockResolvedValue({})
    const onCreated = vi.fn()
    const user = userEvent.setup()

    render(<EventForm onCreated={onCreated} />)

    await user.type(screen.getByLabelText(/sport id/i), ' sport-123 ')
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
      participants: [],
    })
    expect(onCreated).toHaveBeenCalled()
  })

  it('shows validation error when fields are missing', async () => {
    const user = userEvent.setup()
    render(<EventForm />)

    await user.click(screen.getByRole('button', { name: /add event/i }))

    expect(screen.getByText(/sport id is required/i)).toBeInTheDocument()
    expect(mockedCreateEvent).not.toHaveBeenCalled()
  })
})
