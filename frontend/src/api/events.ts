import type { components, paths } from '@api/generated-schema'

import { httpRequest } from './http'

type EventsQuerySchema = NonNullable<paths['/api/v1/events']['get']['parameters']['query']>

export type EventRead = components['schemas']['EventRead']
export type EventCreatePayload = components['schemas']['EventCreate']
export type EventStatus = components['schemas']['EventStatus']
export type EventParticipantRole = components['schemas']['EventParticipantRole']
export type OrderDirection = components['schemas']['OrderDirection']

export type EventsQuery = EventsQuerySchema

export const ORDER_DIRECTIONS: OrderDirection[] = ['asc', 'desc']

export const defaultEventFilters: EventsQuery = {
  order: ORDER_DIRECTIONS[0],
  page: 1,
  page_size: 20,
}

export const listEvents = async (
  filters: Partial<EventsQuery> = {},
  { signal }: { signal?: AbortSignal } = {},
): Promise<EventRead[]> => {
  const query = {
    ...defaultEventFilters,
    ...filters,
  }

  return httpRequest<EventRead[]>('/events', { query, signal })
}

export const createEvent = async (payload: EventCreatePayload): Promise<EventRead> => {
  return httpRequest<EventRead>('/events', {
    method: 'POST',
    body: payload,
  })
}

export const getEvent = async (eventId: string): Promise<EventRead> => {
  return httpRequest<EventRead>(`/events/${eventId}`)
}
