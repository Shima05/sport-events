import { useCallback, useEffect, useMemo, useState } from 'react'

import { defaultEventFilters, listEvents, type EventRead, type EventsQuery } from '@api/events'

const isAbortError = (error: unknown): boolean =>
  error instanceof DOMException && error.name === 'AbortError'

export interface UseEventsResult {
  events: EventRead[]
  loading: boolean
  error: unknown
  filters: EventsQuery
  setFilters: (patch: Partial<EventsQuery>) => void
  refresh: () => Promise<void>
}

export const useEvents = (initialFilters: Partial<EventsQuery> = {}): UseEventsResult => {
  const [filters, setFiltersState] = useState<EventsQuery>({
    ...defaultEventFilters,
    ...initialFilters,
  })
  const [events, setEvents] = useState<EventRead[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<unknown>(null)

  const normalizedFilters = useMemo(() => ({ ...defaultEventFilters, ...filters }), [filters])

  const fetchEvents = useCallback(
    async (options?: { overrides?: Partial<EventsQuery>; signal?: AbortSignal }) => {
      const merged = { ...normalizedFilters, ...(options?.overrides ?? {}) }
      return listEvents(merged, { signal: options?.signal })
    },
    [normalizedFilters],
  )

  const refresh = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetchEvents()
      setEvents(data)
      setError(null)
    } catch (err) {
      if (!isAbortError(err)) {
        setError(err)
        throw err
      }
    } finally {
      setLoading(false)
    }
  }, [fetchEvents])

  useEffect(() => {
    const controller = new AbortController()
    setLoading(true)
    fetchEvents({ signal: controller.signal })
      .then((data) => {
        setEvents(data)
        setError(null)
      })
      .catch((err) => {
        if (!isAbortError(err)) {
          setError(err)
        }
      })
      .finally(() => {
        setLoading(false)
      })

    return () => controller.abort()
  }, [fetchEvents])

  const setFilters = useCallback((patch: Partial<EventsQuery>) => {
    const shouldResetPage = Object.keys(patch).some((key) => key !== 'page')

    setFiltersState((prev) => ({
      ...prev,
      ...patch,
      page: patch.page ?? (shouldResetPage ? 1 : prev.page),
    }))
  }, [])

  return {
    events,
    loading,
    error,
    filters: normalizedFilters,
    setFilters,
    refresh,
  }
}
