# 经营驾驶舱（ERP Dashboard + AI总结）— 模块计划

## 项目概述
为老板开发一套Web端经营数据可视化系统，从定制ERP（阿里云RDS）实时读取数据，
生成6大板块经营图表 + AI智能经营总结。

**技术栈**：Python FastAPI + React + ECharts + DeepSeek API + SQLite + Docker

## 全局架构
见 `project-state/architecture.md`

## 模块拆分

### 模块 1：数据库连接与数据查询层
**目标**：建立ERP数据库只读连接，自动映射现有表结构，提供统一查询接口

**输入**：ERP数据库连接信息（环境变量注入）

**输出**：SQLAlchemy engine（只读）+ ERP表反射模型 + 基础查询工具

**影响文件**：
- `backend/app/config.py`
- `backend/app/core/database.py`
- `backend/app/core/erp_client.py`
- `backend/app/models/erp_models.py`

**依赖关系**：无前置模块

**验收标准**：
- 从环境变量读取ERP数据库连接并连接成功
- 打印现有表清单
- 能执行SELECT查询并返回结果
- 写操作（INSERT/UPDATE/DELETE）被拦截

---

### 模块 2：指标计算引擎（6大板块）
**目标**：将ERP原始数据计算为6大板块经营指标，输出标准化JSON

**输入**：模块1的ERP查询接口

**输出**：6个板块指标JSON（当前值、同比、环比、趋势）

**影响文件**：
- `backend/app/schemas/indicators.py`
- `backend/app/services/revenue.py`
- `backend/app/services/cashflow.py`
- `backend/app/services/inventory.py`
- `backend/app/services/sales.py`
- `backend/app/services/hr.py`
- `backend/app/services/cost.py`
- `backend/app/routers/dashboard.py`

**依赖关系**：前置模块1

**验收标准**：
- API `/api/dashboard/{板块}` 返回200
- 含当前值、同比、环比、12个月趋势
- 查询超时5秒设置

---

### 模块 3：前端仪表面板
**目标**：React页面渲染6板块ECharts图表

**输入**：模块2的API

**输出**：可交互Web仪表盘

**影响文件**：前端全部页面和组件

**依赖关系**：前置模块2

**验收标准**：
- 6板块依次渲染
- loading/错误状态
- 时间范围选择器
- 响应式

---

### 模块 4：AI智能总结 + 自定义调度
**目标**：DeepSeek API经营总结，自定义调度+手动+历史查阅

**输入**：模块2的指标数据

**输出**：总结文本、CRUD接口、调度配置

**影响文件**：
- 后端：ai_summary.py, scheduler.py, local_models.py, routers
- 前端：SummaryPage.tsx, ScheduleConfig.tsx, SummaryCard.tsx

**依赖关系**：前置模块2

**验收标准**：
- 手动触发3-8秒返回
- 调度规则CRUD
- 定时自动执行
- 历史筛选查阅

---

### 模块 5：定时调度器 + 部署 + 认证预留
**目标**：APScheduler集成、Docker部署、JWT认证预留

**输入**：模块3+4的服务

**输出**：docker-compose一键部署

**依赖关系**：前置模块3,4

**验收标准**：
- docker-compose up一键启动
- 调度重启恢复
- JWT可开关

---

## 依赖关系图
```
模块1 → 模块2 → 模块3 → 模块5
              ↘ 模块4 ↗
```

## 实施顺序
模块1 → 模块2 → 模块3 + 模块4(并行) → 模块5
