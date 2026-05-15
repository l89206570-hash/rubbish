/** 应用入口 — 标签页导航：仪表盘 / AI总结 / 调度配置 */

import React, { useState } from 'react'
import { ConfigProvider, Layout, Tabs, theme } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import {
  DashboardOutlined, ThunderboltOutlined, ClockCircleOutlined,
} from '@ant-design/icons'
import Dashboard from './pages/Dashboard'
import SummaryPage from './pages/SummaryPage'
import ScheduleConfig from './pages/ScheduleConfig'

const { Content } = Layout

const App: React.FC = () => {
  const [tab, setTab] = useState('dashboard')

  const items = [
    { key: 'dashboard', label: '经营驾驶舱', icon: <DashboardOutlined />, children: <Dashboard /> },
    { key: 'summary', label: 'AI 总结', icon: <ThunderboltOutlined />, children: <SummaryPage /> },
    { key: 'schedules', label: '调度配置', icon: <ClockCircleOutlined />, children: <ScheduleConfig /> },
  ]

  return (
    <ConfigProvider locale={zhCN} theme={{ algorithm: theme.defaultAlgorithm }}>
      <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
        <Content style={{ padding: '8px 24px', maxWidth: 1400, margin: '0 auto', width: '100%' }}>
          <Tabs activeKey={tab} onChange={setTab} items={items} size="large" />
        </Content>
      </Layout>
    </ConfigProvider>
  )
}

export default App
