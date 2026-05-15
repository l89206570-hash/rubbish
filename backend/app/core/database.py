"""本地数据库引擎 — 驾驶舱自身数据存储（SQLite）"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import config

local_engine = create_engine(
    config.local_db_url,
    connect_args={"check_same_thread": False} if "sqlite" in config.local_db_url else {},
    echo=config.debug,
)

LocalSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=local_engine)

Base = declarative_base()


def get_local_db():
    """FastAPI 依赖注入：获取本地数据库会话"""
    db = LocalSessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_local_db():
    """创建本地数据库所有表"""
    # 延迟导入避免循环引用
    from app.models.local_models import SummaryRecord, ScheduleRule  # noqa: F401
    Base.metadata.create_all(bind=local_engine)
