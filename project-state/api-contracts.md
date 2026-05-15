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
