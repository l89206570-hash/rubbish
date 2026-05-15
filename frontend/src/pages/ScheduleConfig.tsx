/** 调度配置页 — 新增/编辑/暂停/删除调度规则 */

import React, { useState, useEffect, useCallback } from 'react'
import {
  Card, Button, Table, Switch, Modal, Form, Input, Select, message, Space, Popconfirm,
} from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import dayjs from 'dayjs'

const BASE = '/api'

interface ScheduleRule {
  id: number
  name: string
  enabled: boolean
  cron_expression: string
  period_type: string
  board_scope: string
  created_at: string
}

const PERIOD_OPTIONS = [
  { value: 'daily', label: '每日' },
  { value: 'weekly', label: '每周' },
  { value: 'monthly', label: '每月' },
  { value: 'quarterly', label: '每季' },
  { value: 'yearly', label: '每年' },
]

const CRON_PRESETS: Record<string, string> = {
  daily: '0 8 * * *',
  weekly: '0 17 * * 5',
  monthly: '0 9 1 * *',
  quarterly: '0 9 1 1,4,7,10 *',
  yearly: '0 9 1 1 *',
}

const ScheduleConfig: React.FC = () => {
  const [rules, setRules] = useState<ScheduleRule[]>([])
  const [loading, setLoading] = useState(false)
  const [modalOpen, setModalOpen] = useState(false)
  const [form] = Form.useForm()

  const fetchRules = useCallback(async () => {
    setLoading(true)
    try {
      const res = await fetch(`${BASE}/schedules`)
      if (!res.ok) throw new Error(`请求失败: ${res.status}`)
      setRules(await res.json())
    } catch {
      message.error('加载调度规则失败')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { fetchRules() }, [fetchRules])

  const handleCreate = async (values: Record<string, string>) => {
    try {
      const res = await fetch(`${BASE}/schedules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      if (!res.ok) throw new Error('创建失败')
      message.success('调度规则已创建')
      setModalOpen(false)
      form.resetFields()
      fetchRules()
    } catch {
      message.error('创建失败')
    }
  }

  const handleToggle = async (rule: ScheduleRule) => {
    try {
      await fetch(`${BASE}/schedules/${rule.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled: !rule.enabled }),
      })
      fetchRules()
    } catch {
      message.error('操作失败')
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await fetch(`${BASE}/schedules/${id}`, { method: 'DELETE' })
      message.success('规则已删除')
      fetchRules()
    } catch {
      message.error('删除失败')
    }
  }

  const columns = [
    {
      title: '规则名称', dataIndex: 'name', key: 'name',
    },
    {
      title: '周期', dataIndex: 'period_type', key: 'period_type',
      render: (v: string) => PERIOD_OPTIONS.find(o => o.value === v)?.label || v,
    },
    {
      title: 'Cron 表达式', dataIndex: 'cron_expression', key: 'cron_expression',
    },
    {
      title: '状态', dataIndex: 'enabled', key: 'enabled',
      render: (_: boolean, record: ScheduleRule) => (
        <Switch checked={record.enabled} onChange={() => handleToggle(record)} />
      ),
    },
    {
      title: '创建时间', dataIndex: 'created_at', key: 'created_at',
      render: (v: string) => dayjs(v).format('MM-DD HH:mm'),
    },
    {
      title: '操作', key: 'action',
      render: (_: unknown, record: ScheduleRule) => (
        <Popconfirm title="确定删除？" onConfirm={() => handleDelete(record.id)}>
          <Button type="link" danger>删除</Button>
        </Popconfirm>
      ),
    },
  ]

  return (
    <div>
      <div style={{
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center', marginBottom: 16,
      }}>
        <h2 style={{ margin: 0, fontSize: 20 }}>调度配置</h2>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalOpen(true)}>
          新增规则
        </Button>
      </div>

      <Card>
        <Table
          dataSource={rules}
          columns={columns}
          rowKey="id"
          loading={loading}
          pagination={false}
        />
      </Card>

      <Modal
        title="新增调度规则"
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="name" label="规则名称" rules={[{ required: true }]}>
            <Input placeholder="例：每日经营报告" />
          </Form.Item>
          <Form.Item name="period_type" label="周期类型" rules={[{ required: true }]}>
            <Select
              options={PERIOD_OPTIONS}
              onChange={(v) => form.setFieldValue('cron_expression', CRON_PRESETS[v] || '')}
            />
          </Form.Item>
          <Form.Item name="cron_expression" label="Cron 表达式" rules={[{ required: true }]}>
            <Input placeholder="0 8 * * *" />
          </Form.Item>
          <Form.Item name="board_scope" label="板块范围" initialValue="all">
            <Input placeholder="all 或逗号分隔" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ScheduleConfig
