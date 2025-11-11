import { useEffect, useState } from 'react'

import { listTeams, type TeamRead } from '@api/teams'

export const useTeams = (sportId: string | null | undefined) => {
  const [teams, setTeams] = useState<TeamRead[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<unknown>(null)

  useEffect(() => {
    if (!sportId) {
      setTeams([])
      setLoading(false)
      setError(null)
      return
    }

    let cancelled = false
    setLoading(true)
    listTeams({ sport_id: sportId })
      .then((data) => {
        if (!cancelled) {
          setTeams(data)
          setError(null)
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err)
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false)
        }
      })

    return () => {
      cancelled = true
    }
  }, [sportId])

  return { teams, loading, error }
}
