import { useState, useEffect, useCallback } from 'react'
import type { DashboardSummary } from '../types'
import { fetchAllBoards } from '../services/api'

interface UseDashboardResult {
  data: DashboardSummary | null
  loading: boolean
  error: string | null
  period: string
  setPeriod: (p: string) => void
  refresh: () => void
}

export function useDashboard(): UseDashboardResult {
  const [data, setData] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [period, setPeriod] = useState('current')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await fetchAllBoards(period)
      setData(result)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '未知错误')
    } finally {
      setLoading(false)
    }
  }, [period])

  useEffect(() => {
    load()
  }, [load])

  return { data, loading, error, period, setPeriod, refresh: load }
}
