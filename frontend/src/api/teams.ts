import type { components, paths } from '@api/generated-schema'

import { httpRequest } from './http'

export type TeamRead = components['schemas']['TeamRead']

export type TeamListQuery = Partial<
  NonNullable<paths['/api/v1/teams']['get']['parameters']['query']>
>

export const listTeams = (params: TeamListQuery = {}): Promise<TeamRead[]> =>
  httpRequest('/teams', { query: params })
