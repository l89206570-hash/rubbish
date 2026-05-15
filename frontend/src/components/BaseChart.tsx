/** 基础图表包装：loading + 错误 + ECharts 渲染 */

import React from 'react'
import ReactEChartsCore from 'echarts-for-react'
import { Card, Spin, Typography } from 'antd'
import type { EChartsOption } from 'echarts'

const { Text } = Typography

interface BaseChartProps {
  title: string
  loading: boolean
  error?: string | null
  option: EChartsOption | null
  height?: number
  extra?: React.ReactNode
}

const BaseChart: React.FC<BaseChartProps> = ({
  title, loading, error, option, height = 300, extra,
}) => {
  return (
    <Card title={title} style={{ marginBottom: 16 }} extra={extra}>
      {loading ? (
        <div style={{ textAlign: 'center', padding: 60 }}>
          <Spin size="large" />
        </div>
      ) : error ? (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Text type="danger">{error}</Text>
        </div>
      ) : option ? (
        <ReactEChartsCore option={option} style={{ height }} notMerge />
      ) : (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Text type="secondary">暂无数据</Text>
        </div>
      )}
    </Card>
  )
}

export default BaseChart
