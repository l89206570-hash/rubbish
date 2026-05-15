/** 库存折线图（含周转率） */

import React from 'react'
import BaseChart from './BaseChart'
import type { IndicatorResponse } from '../types'
import type { EChartsOption } from 'echarts'

interface Props {
  data?: IndicatorResponse | null
  loading: boolean
  error?: string | null
}

const InventoryChart: React.FC<Props> = ({ data, loading, error }) => {
  const turnover = data?.extra?.turnover_rate as number | undefined
  const subTitle = turnover ? `周转率: ${turnover.toFixed(1)} 次` : ''

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
          type: 'line',
          data: data.trend.map(t => +(t.value / 10000).toFixed(1)),
          smooth: true,
          areaStyle: { opacity: 0.15 },
          itemStyle: { color: '#fa8c16' },
        }],
      }
    : null

  return (
    <BaseChart
      title={`${data?.title ?? '库存'} | 库存额: ¥${(data?.current_value ?? 0).toLocaleString()}`}
      loading={loading}
      error={error}
      option={option}
      extra={subTitle ? <span style={{ fontSize: 12, color: '#888' }}>{subTitle}</span> : undefined}
    />
  )
}

export default InventoryChart
