/** 销售业绩柱状图 */

import React from 'react'
import BaseChart from './BaseChart'
import type { IndicatorResponse } from '../types'
import type { EChartsOption } from 'echarts'

interface Props {
  data?: IndicatorResponse | null
  loading: boolean
  error?: string | null
}

const SalesChart: React.FC<Props> = ({ data, loading, error }) => {
  const customers = data?.extra?.customer_count as number | undefined
  const repeat = data?.extra?.repeat_rate as number | undefined
  const subTitle = customers && repeat
    ? `客户: ${customers}  |  复购率: ${repeat}%`
    : ''

  const option: EChartsOption | null = data?.trend
    ? {
        tooltip: { trigger: 'axis' },
        grid: { left: 60, right: 20, bottom: 30 },
        xAxis: {
          type: 'category',
          data: data.trend.map(t => t.month.slice(5)),
        },
        yAxis: { type: 'value', axisLabel: { formatter: '{value} 万' } },
        series: [{
          type: 'bar',
          data: data.trend.map(t => +(t.value / 10000).toFixed(1)),
          itemStyle: { color: '#722ed1' },
        }],
      }
    : null

  return (
    <BaseChart
      title={`${data?.title ?? '销售'} | ¥${(data?.current_value ?? 0).toLocaleString()}`}
      loading={loading}
      error={error}
      option={option}
      extra={subTitle ? <span style={{ fontSize: 12, color: '#888' }}>{subTitle}</span> : undefined}
    />
  )
}

export default SalesChart
