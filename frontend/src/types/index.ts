/** 单个趋势点 */
export interface TrendPoint {
  month: string
  value: number
}

/** 板块指标响应 */
export interface IndicatorResponse {
  board: string
  title: string
  current_value: number | null
  previous_value: number | null
  yoy_change: number | null
  mom_change: number | null
  trend: TrendPoint[]
  unit: string
  extra: Record<string, unknown>
}

/** 6大板块聚合响应 */
export interface DashboardSummary {
  revenue: IndicatorResponse
  cashflow: IndicatorResponse
  inventory: IndicatorResponse
  sales: IndicatorResponse
  hr: IndicatorResponse
  cost: IndicatorResponse
}
