import type { DashboardSummary, IndicatorResponse } from '../types'

const BASE = '/api'

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`请求失败: ${res.status} ${res.statusText}`)
  }
  return res.json()
}

/** 获取全部6大板块数据 */
export function fetchAllBoards(period = 'current'): Promise<DashboardSummary> {
  return fetchJSON<DashboardSummary>(`${BASE}/dashboard?period=${period}`)
}

/** 获取单个板块数据 */
export function fetchBoard(board: string, period = 'current'): Promise<IndicatorResponse> {
  return fetchJSON<IndicatorResponse>(`${BASE}/dashboard/${board}?period=${period}`)
}

/** 健康检查 */
export function fetchHealth(): Promise<{ status: string; mock_mode: boolean }> {
  return fetchJSON(`${BASE}/health`)
}
