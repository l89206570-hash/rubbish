/** 人效折线图 */

import React from 'react'
import BaseChart from './BaseChart'
import type { IndicatorResponse } from '../types'
import type { EChartsOption } from 'echarts'

interface Props {
  data?: IndicatorResponse | null
  loading: boolean
  error?: string | null
}

const HRChart: React.FC<Props> = ({ data, loading, error }) => {
  const headcount = data?.extra?.headcount as number | undefined
  const avgSalary = data?.extra?.avg_salary as number | undefined
  const turnover = data?.extra?.turnover_rate as number | undefined
  const subTitle = headcount && avgSalary
    ? `在编: ${headcount} 人  |  均薪: ¥${avgSalary.toLocaleString()}  |  离职率: ${turnover}%`
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
          type: 'line',
          data: data.trend.map(t => +(t.value / 10000).toFixed(1)),
          smooth: true,
          areaStyle: { opacity: 0.15 },
          itemStyle: { color: '#13c2c2' },
        }],
      }
    : null

  return (
    <BaseChart
      title={`${data?.title ?? '人效'} | 人均产值 ¥${(data?.current_value ?? 0).toLocaleString()}`}
      loading={loading}
      error={error}
      option={option}
      extra={subTitle ? <span style={{ fontSize: 12, color: '#888' }}>{subTitle}</span> : undefined}
    />
  )
}

export default HRChart
