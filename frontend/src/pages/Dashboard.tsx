/** 仪表盘主页 — 6大板块图表 */

import React from 'react'
import { Row, Col, Select, Alert, Button } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import { useDashboard } from '../hooks/useDashboard'
import RevenueChart from '../components/RevenueChart'
import CashflowChart from '../components/CashflowChart'
import InventoryChart from '../components/InventoryChart'
import SalesChart from '../components/SalesChart'
import HRChart from '../components/HRChart'
import CostChart from '../components/CostChart'

const Dashboard: React.FC = () => {
  const { data, loading, error, period, setPeriod, refresh } = useDashboard()

  return (
    <div style={{ padding: '0 4px' }}>
      {/* 顶栏：标题 + 时间筛选 + 刷新 */}
      <div style={{
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 8,
      }}>
        <h2 style={{ margin: 0, fontSize: 20 }}>经营驾驶舱</h2>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <Select
            value={period}
            onChange={setPeriod}
            style={{ width: 140 }}
            options={[
              { value: 'current', label: '本月' },
              { value: 'quarter', label: '本季' },
              { value: 'year', label: '本年' },
            ]}
          />
          <Button icon={<ReloadOutlined />} onClick={refresh} loading={loading}>
            刷新
          </Button>
        </div>
      </div>

      {/* 全局错误提示 */}
      {error && (
        <Alert
          message="数据加载失败"
          description={error}
          type="error"
          showIcon
          closable
          style={{ marginBottom: 16 }}
        />
      )}

      {/* 图表网格：2行3列 */}
      <Row gutter={[16, 0]}>
        <Col xs={24} lg={12}>
          <RevenueChart data={data?.revenue} loading={loading} error={error} />
        </Col>
        <Col xs={24} lg={12}>
          <CashflowChart data={data?.cashflow} loading={loading} error={error} />
        </Col>
      </Row>
      <Row gutter={[16, 0]}>
        <Col xs={24} lg={12}>
          <InventoryChart data={data?.inventory} loading={loading} error={error} />
        </Col>
        <Col xs={24} lg={12}>
          <SalesChart data={data?.sales} loading={loading} error={error} />
        </Col>
      </Row>
      <Row gutter={[16, 0]}>
        <Col xs={24} lg={12}>
          <HRChart data={data?.hr} loading={loading} error={error} />
        </Col>
        <Col xs={24} lg={12}>
          <CostChart data={data?.cost} loading={loading} error={error} />
        </Col>
      </Row>
    </div>
  )
}

export default Dashboard
