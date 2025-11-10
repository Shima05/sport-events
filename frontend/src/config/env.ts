const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1'

const normalizeBaseUrl = (raw?: string): string => {
  if (!raw) {
    return DEFAULT_API_BASE_URL
  }

  return raw.endsWith('/') ? raw.slice(0, -1) : raw
}

export const env = {
  apiBaseUrl: normalizeBaseUrl(import.meta.env.VITE_API_BASE_URL),
}

export type EnvConfig = typeof env
