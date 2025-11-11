import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { defaultEventFilters } from '@api/events'
import { useSports } from '@hooks/useSports'

import { EventFilters } from './EventFilters'

vi.mock('@hooks/useSports', () => ({
  useSports: vi.fn(),
}))

const mockedUseSports = useSports as unknown as ReturnType<typeof vi.fn>

describe('EventFilters', () => {
  beforeEach(() => {
    mockedUseSports.mockReset()
    mockedUseSports.mockReturnValue({ sports: [], loading: false, error: null })
  })

  it('submits normalized filters', async () => {
    const handleApply = vi.fn()
    const handleReset = vi.fn()
    const user = userEvent.setup()

    mockedUseSports.mockReturnValue({
      sports: [
        { id: 'sport-1', name: 'Football', code: 'football' },
        { id: 'sport-2', name: 'Basketball', code: 'basketball' },
      ],
      loading: false,
      error: null,
    })

    render(
      <EventFilters filters={defaultEventFilters} onApply={handleApply} onReset={handleReset} />,
    )

    await user.selectOptions(screen.getByLabelText(/^sport/i), 'sport-2')
    await user.selectOptions(screen.getByLabelText(/order/i), 'desc')

    await user.click(screen.getByRole('button', { name: /apply filters/i }))

    expect(handleApply).toHaveBeenCalledWith(
      expect.objectContaining({
        sport_id: 'sport-2',
        order: 'desc',
        page: 1,
      }),
    )
  })

  it('resets the form', async () => {
    const handleApply = vi.fn()
    const handleReset = vi.fn()
    const user = userEvent.setup()

    render(
      <EventFilters filters={defaultEventFilters} onApply={handleApply} onReset={handleReset} />,
    )

    await user.type(screen.getByLabelText(/^sport/i), 'something')
    await user.click(screen.getByRole('button', { name: /reset/i }))

    expect(handleReset).toHaveBeenCalled()
    expect(screen.getByLabelText(/^sport/i)).toHaveValue('')
  })
})
