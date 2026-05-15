/** AI 总结展示卡片 */

import React from 'react'
import { Card, Tag, Typography } from 'antd'
import dayjs from 'dayjs'

const { Text, Paragraph } = Typography

interface SummaryRecord {
  id: number
  content: string
  board_scope: string
  period_type: string
  period_start: string
  period_end: string
  trigger_type: string
  created_at: string
}

const PERIOD_LABELS: Record<string, string> = {
  daily: '日报',
  weekly: '周报',
  monthly: '月报',
  quarterly: '季报',
  yearly: '年报',
  custom: '自定义',
}

const SummaryCard: React.FC<{ record: SummaryRecord }> = ({ record }) => {
  return (
    <Card
      size="small"
      style={{ marginBottom: 12 }}
      title={
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span>{PERIOD_LABELS[record.period_type] || record.period_type}</span>
          <Tag color={record.trigger_type === 'auto' ? 'blue' : 'green'}>
            {record.trigger_type === 'auto' ? '自动生成' : '手动'}
          </Tag>
        </div>
      }
      extra={
        <Text type="secondary" style={{ fontSize: 12 }}>
          {dayjs(record.created_at).format('MM-DD HH:mm')}
        </Text>
      }
    >
      <Paragraph
        style={{ whiteSpace: 'pre-wrap', margin: 0, fontSize: 13 }}
      >
        {record.content}
      </Paragraph>
    </Card>
  )
}

export default SummaryCard
