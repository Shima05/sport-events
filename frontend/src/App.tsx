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

  const canGoNext = events.length === (filters.page_size ?? defaultEventFilters.page_size)

  return (
    <AppLayout>
      <section className="page-hero" id="events">
        <div>
          <p className="eyebrow">Sports calendar</p>
          <h1>Track every upcoming match in one place</h1>
          <p className="muted">
            Query the FastAPI backend in real time, filter by sport or date range and keep an eye on
            the fixtures that matter.
          </p>
        </div>
        <button type="button" className="primary" onClick={handleRefresh} disabled={loading}>
          Refresh events
        </button>
      </section>

      <section className="split-panels">
        <EventFilters
          filters={filters}
          onApply={handleApplyFilters}
          onReset={handleResetFilters}
          disabled={loading}
        />
        <EventForm onCreated={handleRefresh} />
      </section>
      <EventList events={events} loading={loading} error={error} />

      <PaginationControls
        page={filters.page ?? 1}
        pageSize={filters.page_size ?? defaultEventFilters.page_size}
        canGoNext={canGoNext}
        loading={loading}
        onPageChange={handlePageChange}
      />
    </AppLayout>
  )
}

export default App
