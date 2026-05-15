# 模块 2 完成摘要：指标计算引擎（6大板块）

## 完成时间
2026-05-15T22:35:00+08:00

## 已完成内容
- `schemas/indicators.py` — 统一指标响应格式（IndicatorResponse、TrendPoint、DashboardSummary）
- 6个板块计算服务，统一接口 `calculate(period) -> IndicatorResponse`
- `routers/dashboard.py` — 单板块查询 `GET /api/dashboard/{board}` 和全板块聚合 `GET /api/dashboard`

## 新增接口
- `GET /api/dashboard` — 返回全部6大板块数据
- `GET /api/dashboard/{board}` — 返回单个板块（revenue/cashflow/inventory/sales/hr/cost）
- 每个板块含：current_value, previous_value, yoy_change, mom_change, trend, extra

## 修改的文件
- `backend/app/schemas/__init__.py`
- `backend/app/schemas/indicators.py`
- `backend/app/services/__init__.py`
- `backend/app/services/revenue.py`
- `backend/app/services/cashflow.py`
- `backend/app/services/inventory.py`
- `backend/app/services/sales.py`
- `backend/app/services/hr.py`
- `backend/app/services/cost.py`
- `backend/app/routers/__init__.py`
- `backend/app/routers/dashboard.py`
- `backend/app/main.py`（添加dashboard路由注册）

## 遗留问题
- 无
