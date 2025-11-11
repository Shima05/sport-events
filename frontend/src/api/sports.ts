import type { components } from '@api/generated-schema'

import { httpRequest } from './http'

export type SportRead = components['schemas']['SportRead']

export const listSports = async (): Promise<SportRead[]> => httpRequest('/sports')
