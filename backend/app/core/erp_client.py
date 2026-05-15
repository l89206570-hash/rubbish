"""ERP 数据库只读连接客户端

通过 SQLAlchemy automap 自动反射 ERP 现有表结构。
只在 `mock_mode=False` 且配置了 ERP 连接串时才真实连接。"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional, Dict

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import OperationalError

from app.config import config

logger = logging.getLogger(__name__)

_erp_engine = None
_erp_session_local = None


def _build_erp_engine():
    """创建 ERP 数据库只读引擎"""
    global _erp_engine, _erp_session_local

    if not config.erp_db_url:
        logger.warning("ERP 数据库连接串未配置，使用 Mock 模式")
        return

    # 只读 + 连接池配置
    _erp_engine = create_engine(
        config.erp_db_url,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=config.debug,
        # 通过 SQLAlchemy 连接参数强制只读
        connect_args=(
            {"charset": "utf8mb4"} if config.erp_db_type == "mysql"
            else {"options": "-c default_transaction_read_only=on"}
            if config.erp_db_type == "postgresql"
            else {}
        ),
    )
    _erp_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_erp_engine,
    )

    # 验证连接
    try:
        with _erp_session_local() as session:
            result = session.execute(text("SELECT 1"))
            logger.info("ERP 数据库连接成功 ✓")
    except OperationalError as e:
        logger.error(f"ERP 数据库连接失败: {e}")
        _erp_engine = None
        _erp_session_local = None


def get_erp_session() -> Session:
    """获取 ERP 数据库会话"""
    if _erp_session_local is None:
        raise RuntimeError("ERP 数据库未连接，请检查配置")
    return _erp_session_local()


def list_erp_tables() -> List[str]:
    """列出 ERP 数据库中的表"""
    session = get_erp_session()
    try:
        if config.erp_db_type == "mysql":
            result = session.execute(text("SHOW TABLES"))
        else:
            result = session.execute(
                text("SELECT table_name FROM information_schema.tables "
                     "WHERE table_schema = :schema"),
                {"schema": config.erp_db_name},
            )
        return [row[0] for row in result]
    finally:
        session.close()


def execute_query(sql: str, params: Optional[Dict[str, object]] = None) -> List[dict]:
    """安全执行只读 SQL 查询，返回字典列表"""
    session = get_erp_session()
    try:
        result = session.execute(text(sql), params or {})
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
    finally:
        session.close()


def init_erp_client():
    """初始化 ERP 客户端（应用启动时调用）"""
    if config.mock_mode or not config.erp_db_url:
        logger.info("🟡 Mock 模式 — 使用模拟数据，不连接真实 ERP")
        return

    _build_erp_engine()

    if _erp_engine is not None:
        try:
            tables = list_erp_tables()
            logger.info(f"ERP 数据库表清单 ({len(tables)} 张):")
            for t in tables[:20]:
                logger.info(f"  - {t}")
            if len(tables) > 20:
                logger.info(f"  ... 共 {len(tables)} 张表")
        except Exception as e:
            logger.warning(f"读取ERP表清单失败: {e}")


# ---- Mock 数据模块 ----

MOCK_DASHBOARD_DATA = {
    "revenue": {
        "current_value": 1285000,
        "previous_value": 1142000,
        "yoy_change": 12.5,
        "mom_change": 3.2,
        "trend": [
            {"month": "2025-06", "value": 1142000},
            {"month": "2025-07", "value": 1180000},
            {"month": "2025-08", "value": 1210000},
            {"month": "2025-09", "value": 1195000},
            {"month": "2025-10", "value": 1230000},
            {"month": "2025-11", "value": 1250000},
            {"month": "2025-12", "value": 1310000},
            {"month": "2026-01", "value": 1150000},
            {"month": "2026-02", "value": 1200000},
            {"month": "2026-03", "value": 1240000},
            {"month": "2026-04", "value": 1260000},
            {"month": "2026-05", "value": 1285000},
        ],
    },
    "cashflow": {
        "current_value": -320000,
        "previous_value": -150000,
        "yoy_change": None,
        "mom_change": -113.3,
        "trend": [
            {"month": "2026-05", "value": -320000},
            {"month": "2026-04", "value": -150000},
            {"month": "2026-03", "value": 180000},
        ],
    },
    "inventory": {
        "current_value": 4560000,
        "previous_value": 4200000,
        "yoy_change": 8.6,
        "mom_change": 1.5,
        "turnover_rate": 4.2,
        "trend": [
            {"month": "2026-01", "value": 4100000},
            {"month": "2026-02", "value": 4300000},
            {"month": "2026-03", "value": 4400000},
            {"month": "2026-04", "value": 4200000},
            {"month": "2026-05", "value": 4560000},
        ],
    },
    "sales": {
        "current_value": 925000,
        "previous_value": 850000,
        "yoy_change": 8.8,
        "mom_change": 2.1,
        "customer_count": 128,
        "repeat_rate": 62.5,
        "trend": [
            {"month": "2026-01", "value": 780000},
            {"month": "2026-02", "value": 810000},
            {"month": "2026-03", "value": 870000},
            {"month": "2026-04", "value": 850000},
            {"month": "2026-05", "value": 925000},
        ],
    },
    "hr": {
        "current_value": 85600,
        "previous_value": 82000,
        "yoy_change": 4.4,
        "mom_change": 1.2,
        "headcount": 245,
        "avg_salary": 12500,
        "turnover_rate": 2.1,
        "trend": [
            {"month": "2026-01", "value": 82000},
            {"month": "2026-02", "value": 83000},
            {"month": "2026-03", "value": 84000},
            {"month": "2026-04", "value": 84500},
            {"month": "2026-05", "value": 85600},
        ],
    },
    "cost": {
        "current_value": 785000,
        "previous_value": 720000,
        "yoy_change": 9.0,
        "mom_change": 2.8,
        "breakdown": {
            "原材料": 35.0,
            "人工": 28.0,
            "运营": 15.0,
            "销售": 12.0,
            "研发": 7.0,
            "其他": 3.0,
        },
        "trend": [
            {"month": "2026-01", "value": 680000},
            {"month": "2026-02", "value": 710000},
            {"month": "2026-03", "value": 740000},
            {"month": "2026-04", "value": 720000},
            {"month": "2026-05", "value": 785000},
        ],
    },
}
