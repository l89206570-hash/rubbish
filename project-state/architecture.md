# 当前架构

## 技术栈
- 后端：Python 3.11 + FastAPI + SQLAlchemy 2.0 + APScheduler
- 前端：React 18 + Vite + ECharts 5 + Ant Design 5
- AI：DeepSeek API (openai 兼容模式)
- 数据库：SQLite（驾驶舱本地存储）
- 部署：Docker + docker-compose

## 目录结构
```
erp-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── config.py            # 配置管理（环境变量）
│   │   ├── core/
│   │   │   ├── database.py      # 本地SQLAlchemy引擎
│   │   │   └── erp_client.py    # ERP数据库只读连接
│   │   ├── models/
│   │   │   ├── erp_models.py    # ERP表反射映射
│   │   │   └── local_models.py  # 驾驶舱本地表
│   │   ├── schemas/
│   │   │   ├── indicators.py    # 指标输出schema
│   │   │   ├── summaries.py     # AI总结schema
│   │   │   └── schedules.py     # 调度配置schema
│   │   ├── services/
│   │   │   ├── revenue.py       # 营收利润
│   │   │   ├── cashflow.py      # 现金流
│   │   │   ├── inventory.py     # 库存供应链
│   │   │   ├── sales.py         # 销售客户
│   │   │   ├── hr.py            # 人效人力
│   │   │   ├── cost.py          # 成本结构
│   │   │   ├── ai_summary.py    # AI总结生成
│   │   │   └── scheduler.py     # 定时调度
│   │   ├── routers/
│   │   │   ├── dashboard.py     # 仪表盘数据API
│   │   │   ├── summaries.py     # 总结CRUD
│   │   │   └── schedules.py     # 调度配置API
│   │   └── auth/
│   │       └── jwt.py           # JWT认证（预留）
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── SummaryPage.tsx
│   │   │   └── ScheduleConfig.tsx
│   │   ├── components/
│   │   │   ├── RevenueChart.tsx
│   │   │   ├── CashflowChart.tsx
│   │   │   ├── InventoryChart.tsx
│   │   │   ├── SalesChart.tsx
│   │   │   ├── HRChart.tsx
│   │   │   ├── CostChart.tsx
│   │   │   └── SummaryCard.tsx
│   │   ├── hooks/useDashboard.ts
│   │   ├── services/api.ts
│   │   └── types/index.ts
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── .gitignore
```

## 数据流
```
ERP数据库(RDS/只读) ──SQLAlchemy──→ 指标计算服务(6个) ──JSON──→ React前端(ECharts渲染)
                                           │
                                           ├──→ AI总结服务(DeepSeek) ──→ 本地SQLite
                                           │
                                           └──→ 定时调度器(APScheduler)
```

## 关键设计决策
- **ERP只读连接**：独立账号仅SELECT权限，SQLAlchemy反射映射已有表，不污染ERP库
- **本地SQLite**：驾驶舱自身数据与ERP完全隔离，可随时迁移到PostgreSQL
- **组件分离**：6个板块独立ECharts组件，增删板块不改其他组件
- **AI模板化**：Prompt模板先固定快速落地，预留自定义接口
- **JWT可插拔**：中间件模式，环境变量 `AUTH_ENABLED=false` 跳过认证
- **调度持久化**：APScheduler配置存SQLite，重启自动恢复调度任务
