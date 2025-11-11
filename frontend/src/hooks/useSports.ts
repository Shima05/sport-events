import { useEffect, useState } from 'react'

import { listSports, type SportRead } from '@api/sports'

export const useSports = () => {
  const [sports, setSports] = useState<SportRead[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<unknown>(null)

  useEffect(() => {
    let mounted = true

    listSports()
      .then((data) => {
        if (mounted) {
          setSports(data)
          setError(null)
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(err)
        }
      })
      .finally(() => {
        if (mounted) {
          setLoading(false)
        }
      })

    return () => {
      mounted = false
    }
  }, [])

  return { sports, loading, error }
}
