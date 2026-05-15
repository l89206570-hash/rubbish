/** 营收利润折线图 */

import React from 'react'
import BaseChart from './BaseChart'
import type { IndicatorResponse } from '../types'
import type { EChartsOption } from 'echarts'

interface Props {
  data?: IndicatorResponse | null
  loading: boolean
  error?: string | null
}

const RevenueChart: React.FC<Props> = ({ data, loading, error }) => {
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
          itemStyle: { color: '#1677ff' },
        }],
      }
    : null

  return (
    <BaseChart
      title={`${data?.title ?? '营收利润'} | 当前: ¥${(data?.current_value ?? 0).toLocaleString()}`}
      loading={loading}
      error={error}
      option={option}
    />
  )
}

export default RevenueChart
