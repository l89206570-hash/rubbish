# 经营驾驶舱 (ERP Dashboard + AI 总结)

从定制 ERP（阿里云 RDS）实时读取数据，生成 6 大板块经营图表 + AI 智能经营总结。

## 功能

- **6 大经营板块**：营收利润、现金流、库存供应链、销售客户、人效人力、成本结构
- **实时数据**：每次打开页面直连 ERP 数据库，拉取最新数据
- **ECharts 图表**：折线图、柱状图、饼图，支持时间范围筛选
- **AI 经营总结**：调用 DeepSeek API 自动生成自然语言经营分析报告
- **自定义调度**：日/周/月/季/年自动生成总结，支持自定义 cron 表达式
- **多用户预留**：JWT 认证框架（环境变量一键启用）

## 快速启动

### 本地开发

#### 1. 后端

```bash
cd backend
cp .env.example .env    # 编辑配置
pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

#### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000。

### Docker 部署

```bash
# 1. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env，填入 ERP 数据库和 DeepSeek API 信息

# 2. 一键启动
docker-compose up -d

# 3. 访问
# http://localhost:80 — 前端页面
# http://localhost:8000/docs — API 文档
```

## 配置说明

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `MOCK_MODE` | Mock 模式（无 ERP 时使用模拟数据） | `true` |
| `ERP_DB_HOST` | ERP 数据库地址 | - |
| `ERP_DB_USER` | 只读账号 | - |
| `ERP_DB_PASSWORD` | 密码 | - |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | - |
| `AUTH_ENABLED` | 是否启用 JWT 认证 | `false` |

## 技术栈

- **后端**：Python 3.11 + FastAPI + SQLAlchemy 2.0 + APScheduler
- **前端**：React 18 + TypeScript + Vite + ECharts 5 + Ant Design 5
- **AI**：DeepSeek API（OpenAI 兼容模式）
- **部署**：Docker + docker-compose
