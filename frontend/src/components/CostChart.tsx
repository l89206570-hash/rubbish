/** 成本结构饼图 + 趋势 */

import React from 'react'
import BaseChart from './BaseChart'
import type { IndicatorResponse } from '../types'
import type { EChartsOption } from 'echarts'

interface Props {
  data?: IndicatorResponse | null
  loading: boolean
  error?: string | null
}

const CostChart: React.FC<Props> = ({ data, loading, error }) => {
  const breakdown = data?.extra?.breakdown as Record<string, number> | undefined

  const option: EChartsOption | null = breakdown
    ? {
        tooltip: { trigger: 'item', formatter: '{b}: {d}%' },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%', '50%'],
          data: Object.entries(breakdown).map(([name, value]) => ({ name, value })),
          label: { formatter: '{b}\n{d}%' },
          itemStyle: { borderRadius: 4 },
        }],
      }
    : null

  return (
    <BaseChart
      title={`${data?.title ?? '成本'} | 总计 ¥${(data?.current_value ?? 0).toLocaleString()}`}
      loading={loading}
      error={error}
      option={option}
      height={320}
    />
  )
}

export default CostChart
