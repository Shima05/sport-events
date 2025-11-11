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

const extractDetailMessage = (payload: unknown): string | null => {
  if (!payload) {
    return null
  }
  if (typeof payload === 'string') {
    return payload
  }
  if (typeof payload === 'object') {
    if ('detail' in payload) {
      const detail = (payload as { detail?: unknown }).detail
      if (typeof detail === 'string') {
        return detail
      }
      if (Array.isArray(detail)) {
        const parts = detail
          .map((item) => {
            if (!item) return null
            if (typeof item === 'string') return item
            if (typeof item === 'object' && 'msg' in item && typeof item.msg === 'string')
              return item.msg
            return null
          })
          .filter(Boolean)
        if (parts.length) {
          return parts.join('; ')
        }
      }
    }
    if ('message' in payload && typeof (payload as { message?: unknown }).message === 'string') {
      return (payload as { message: string }).message
    }
  }
  return null
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
    const detail = extractDetailMessage(parsed)
    const fallback = `Request failed with status ${response.status}`
    throw new ApiError(detail ?? fallback, response.status, parsed as TResponse)
  }

  return parsed as TResponse
}
