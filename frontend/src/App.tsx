import { useState } from 'react'

import { defaultEventFilters, type EventsQuery } from '@api/events'
import AppLayout from '@components/AppLayout'
import { EventFilters } from '@components/EventFilters'
import { EventList } from '@components/EventList'
import { EventForm } from '@components/EventForm'
import { PaginationControls } from '@components/PaginationControls'
import { useEvents } from '@hooks/useEvents'
import './App.css'

function App() {
  const { events, loading, error, filters, setFilters, refresh } = useEvents()
  const [isModalOpen, setModalOpen] = useState(false)

  const handleApplyFilters = (nextFilters: EventsQuery) => {
    setFilters({ ...nextFilters, page: 1 })
  }

  const handleResetFilters = () => {
    setFilters(defaultEventFilters)
  }

  const handlePageChange = (nextPage: number) => {
    if (nextPage < 1 || nextPage === (filters.page ?? 1)) {
      return
    }
    setFilters({ page: nextPage })
  }

  const handleRefresh = () => {
    void refresh()
  }

  const openModal = () => setModalOpen(true)
  const closeModal = () => setModalOpen(false)

  const canGoNext = events.length === (filters.page_size ?? defaultEventFilters.page_size)

  return (
    <AppLayout>
      <div className="actions-bar">
        <button type="button" className="secondary" onClick={handleRefresh} disabled={loading}>
          Refresh events
        </button>
        <button type="button" className="primary" onClick={openModal}>
          + Add event
        </button>
      </div>

      <section className="filters-section">
        <EventFilters
          filters={filters}
          onApply={handleApplyFilters}
          onReset={handleResetFilters}
          disabled={loading}
        />
      </section>
      <EventList events={events} loading={loading} error={error} />

      <PaginationControls
        page={filters.page ?? 1}
        pageSize={filters.page_size ?? defaultEventFilters.page_size}
        canGoNext={canGoNext}
        loading={loading}
        onPageChange={handlePageChange}
      />

      {isModalOpen && (
        <div className="modal-backdrop" role="presentation" onClick={closeModal}>
          <div
            className="modal-dialog"
            role="dialog"
            aria-modal="true"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-header">
              <h2>Add a new event</h2>
              <button type="button" className="icon-button" onClick={closeModal} aria-label="Close">
                ×
              </button>
            </div>
            <EventForm
              onCreated={async () => {
                await refresh()
                closeModal()
              }}
            />
          </div>
        </div>
      )}
    </AppLayout>
  )
}

export default App
