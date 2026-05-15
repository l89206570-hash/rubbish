/** AI 总结页面 — 手动生成 + 历史查阅 */

import React, { useState, useEffect, useCallback } from 'react'
import {
  Card, Button, DatePicker, Select, Space, Spin, Alert, Empty, Tag, Typography,
} from 'antd'
import { ThunderboltOutlined, ReloadOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'
import SummaryCard from '../components/SummaryCard'

const { RangePicker } = DatePicker
const { Text } = Typography

const BASE = '/api'

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

const PERIOD_OPTIONS = [
  { value: '', label: '全部' },
  { value: 'daily', label: '日报' },
  { value: 'weekly', label: '周报' },
  { value: 'monthly', label: '月报' },
  { value: 'quarterly', label: '季报' },
  { value: 'yearly', label: '年报' },
]

const SummaryPage: React.FC = () => {
  const [summaries, setSummaries] = useState<SummaryRecord[]>([])
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [periodType, setPeriodType] = useState<string>('')
  const [dates, setDates] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null)

  const fetchSummaries = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      if (periodType) params.set('period_type', periodType)
      const res = await fetch(`${BASE}/summaries?${params}`)
      if (!res.ok) throw new Error(`请求失败: ${res.status}`)
      const data = await res.json()
      setSummaries(data.items || [])
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '加载失败')
    } finally {
      setLoading(false)
    }
  }, [periodType])

  useEffect(() => { fetchSummaries() }, [fetchSummaries])

  const handleGenerate = async () => {
    if (!dates || !dates[0] || !dates[1]) return
    setGenerating(true)
    try {
      const res = await fetch(`${BASE}/summaries/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          period_type: 'custom',
          period_start: dates[0].format('YYYY-MM-DD'),
          period_end: dates[1].format('YYYY-MM-DD'),
          board_scope: 'all',
        }),
      })
      if (!res.ok) throw new Error(`生成失败: ${res.status}`)
      await fetchSummaries()
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : '生成失败')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div>
      <div style={{
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 8,
      }}>
        <h2 style={{ margin: 0, fontSize: 20 }}>AI 经营总结</h2>
        <Space wrap>
          <RangePicker
            value={dates}
            onChange={(v) => setDates(v as [dayjs.Dayjs, dayjs.Dayjs] | null)}
            allowClear
            placeholder={['开始日期', '结束日期']}
          />
          <Button
            type="primary"
            icon={<ThunderboltOutlined />}
            onClick={handleGenerate}
            loading={generating}
            disabled={!dates}
          >
            {generating ? '生成中...' : '生成总结'}
          </Button>
        </Space>
      </div>

      <div style={{ marginBottom: 16 }}>
        <Space>
          <Text type="secondary">筛选：</Text>
          <Select
            value={periodType}
            onChange={setPeriodType}
            style={{ width: 120 }}
            options={PERIOD_OPTIONS}
          />
          <Button icon={<ReloadOutlined />} onClick={fetchSummaries} size="small">
            刷新
          </Button>
        </Space>
      </div>

      {error && (
        <Alert message={error} type="error" showIcon closable style={{ marginBottom: 12 }}
          onClose={() => setError(null)} />
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: 60 }}><Spin size="large" /></div>
      ) : summaries.length === 0 ? (
        <Empty description="暂无总结记录，选择日期范围并点击「生成总结」" />
      ) : (
        summaries.map(s => <SummaryCard key={s.id} record={s} />)
      )}
    </div>
  )
}

export default SummaryPage
