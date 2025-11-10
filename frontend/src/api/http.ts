import { env } from '@config/env'

const toURLSearchParams = (
  query?: Record<string, string | number | boolean | null | undefined>,
): URLSearchParams => {
  const search = new URLSearchParams()
  if (!query) {
    return search
  }

  Object.entries(query).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') {
      return
    }
    search.append(key, String(value))
  })
  return search
}

const buildUrl = (
  path: string,
  query?: Record<string, string | number | boolean | null | undefined>,
): URL => {
  const normalizedPath = path.startsWith('/') ? path.slice(1) : path
  const base = `${env.apiBaseUrl}/`
  const url = new URL(normalizedPath, base)
  const search = toURLSearchParams(query)
  if ([...search.keys()].length) {
    url.search = search.toString()
  }
  return url
}

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

export interface HttpOptions {
  method?: HttpMethod
  query?: Record<string, string | number | boolean | null | undefined>
  body?: unknown
  headers?: Record<string, string>
  signal?: AbortSignal
}

export class ApiError<TBody = unknown> extends Error {
  public readonly status: number
  public readonly body: TBody | null

  constructor(message: string, status: number, body: TBody | null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }
}

const parseResponseBody = async (response: Response): Promise<unknown> => {
  if (response.status === 204) {
    return null
  }

  const contentType = response.headers.get('content-type')
  if (contentType && contentType.includes('application/json')) {
    return response.json()
  }

  return response.text()
}

export const httpRequest = async <TResponse>(
  path: string,
  { method = 'GET', query, body, headers, signal }: HttpOptions = {},
): Promise<TResponse> => {
  const url = buildUrl(path, query)

  const response = await fetch(url, {
    method,
    signal,
    headers: {
      Accept: 'application/json',
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  })

  const parsed = await parseResponseBody(response)

  if (!response.ok) {
    throw new ApiError('Request to API failed', response.status, parsed)
  }

  return parsed as TResponse
}
