import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'

import { defaultEventFilters } from '@api/events'

import { EventFilters } from './EventFilters'

describe('EventFilters', () => {
  it('submits normalized filters', async () => {
    const handleApply = vi.fn()
    const handleReset = vi.fn()
    const user = userEvent.setup()

    render(
      <EventFilters filters={defaultEventFilters} onApply={handleApply} onReset={handleReset} />,
    )

    await user.type(screen.getByLabelText(/sport id/i), 'abc-123')
    await user.selectOptions(screen.getByLabelText(/order/i), 'desc')

    await user.click(screen.getByRole('button', { name: /apply filters/i }))

    expect(handleApply).toHaveBeenCalledWith(
      expect.objectContaining({
        sport_id: 'abc-123',
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

    await user.type(screen.getByLabelText(/sport id/i), 'something')
    await user.click(screen.getByRole('button', { name: /reset/i }))

    expect(handleReset).toHaveBeenCalled()
    expect(screen.getByLabelText(/sport id/i)).toHaveValue('')
  })
})
