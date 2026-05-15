"""ERP 数据库表模型 — 使用 SQLAlchemy automap 自动反射

当连接真实 ERP 数据库时，通过 automap 自动将现有表映射为 ORM 模型。
当前仅在 `MOCK_MODE=True` 时不生效（使用 mock 数据）。"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import MetaData

from app.config import config
from app.core.erp_client import get_erp_session, _erp_engine

# automap base — 后续模块通过反射得到的模型操作 ERP 数据
ERPBase = automap_base()

# 存储反射得到的模型类，供其他模块引用
ERPModels: dict = {}


def reflect_erp_tables():
    """反射 ERP 数据库中所有表，生成 ORM 模型

    如果表结构复杂或数量过多，可改为只反射指定表。
    """
    global ERPModels

    if config.mock_mode or _erp_engine is None:
        return

    ERPBase.prepare(autoload_with=_erp_engine)

    # 将反射到的模型存入字典，供其他模块通过名称引用
    for table_name, model_class in ERPBase.classes.items():
        ERPModels[table_name] = model_class
