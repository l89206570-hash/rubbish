/** 现金流柱状图 */

import React from 'react'
import BaseChart from './BaseChart'
import type { IndicatorResponse } from '../types'
import type { EChartsOption } from 'echarts'

interface Props {
  data?: IndicatorResponse | null
  loading: boolean
  error?: string | null
}

const CashflowChart: React.FC<Props> = ({ data, loading, error }) => {
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
          itemStyle: (params: { value: number }) => ({
            color: params.value >= 0 ? '#52c41a' : '#ff4d4f',
          }),
        }],
      }
    : null

  return (
    <BaseChart
      title={`${data?.title ?? '现金流'} | 当前: ¥${(data?.current_value ?? 0).toLocaleString()}`}
      loading={loading}
      error={error}
      option={option}
    />
  )
}

export default CashflowChart
