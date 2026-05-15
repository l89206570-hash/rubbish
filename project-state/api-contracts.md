# 接口契约

各模块间显式接口契约在此记录。

## 模块1 → 模块2+
| 函数/端点 | 签名 | 说明 |
|-----------|------|------|
| health_check | `GET /api/health` | 健康检查 |
| get_erp_session | `app.core.erp_client.get_erp_session() -> Session` | ERP数据库会话 |
| execute_query | `app.core.erp_client.execute_query(sql, params) -> list[dict]` | 只读SQL查询 |
| list_erp_tables | `app.core.erp_client.list_erp_tables() -> list[str]` | 列出ERP表 |
| get_local_db | `app.core.database.get_local_db() -> Generator[Session]` | 本地数据库（FastAPI依赖注入） |
| config | `app.config.config -> Config` | 全局配置对象 |
| MOCK_DATA | `app.core.erp_client.MOCK_DASHBOARD_DATA -> dict` | 6大板块Mock数据 |
| init_erp_client | `app.core.erp_client.init_erp_client()` | 启动时初始化ERP连接 |
| init_local_db | `app.core.database.init_local_db()` | 启动时初始化本地库 |

## 模块2 → 模块3+
| 函数/端点 | 签名 | 说明 |
|-----------|------|------|
| get_all_boards | `GET /api/dashboard?period=current` | 返回6大板块完整指标数据 |
| get_board | `GET /api/dashboard/{board}?period=current` | 返回单个板块指标 |
| IndicatorResponse | `board, title, current_value, yoy_change, mom_change, trend, unit, extra` | 标准化指标响应格式 |
| DashboardSummary | `{revenue, cashflow, inventory, sales, hr, cost}` | 聚合响应格式 |
| calc_{板块} | `services.{板块}.calculate(period) -> IndicatorResponse` | 各板块计算函数 |

## 模块3 → 模块5（前端API调用约定）
| 端点 | 说明 |
|------|------|
| `GET /api/dashboard?period=current` | 后端提供，前端通过Vite proxy `/api` → `localhost:8000` |
