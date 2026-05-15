/** 应用入口 — 仪表盘单页 */

import React from 'react'
import { ConfigProvider, Layout, theme } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import Dashboard from './pages/Dashboard'

const { Content } = Layout

const App: React.FC = () => {
  return (
    <ConfigProvider locale={zhCN} theme={{ algorithm: theme.defaultAlgorithm }}>
      <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
        <Content style={{ padding: '16px 24px', maxWidth: 1400, margin: '0 auto' }}>
          <Dashboard />
        </Content>
      </Layout>
    </ConfigProvider>
  )
}

export default App
