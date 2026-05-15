"""驾驶舱本地数据模型 — SQLite 存储：总结记录、调度规则"""

import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from app.core.database import Base


class SummaryRecord(Base):
    """AI 总结记录"""
    __tablename__ = "summary_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)                  # 总结正文（Markdown）
    board_scope = Column(String(200), default="all")         # 板块范围
    period_type = Column(String(20), nullable=False)         # daily | weekly | monthly | quarterly | yearly | custom
    period_start = Column(String(10), nullable=False)        # 2026-05-01
    period_end = Column(String(10), nullable=False)          # 2026-05-15
    trigger_type = Column(String(20), default="manual")      # manual | auto
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class ScheduleRule(Base):
    """自定义调度规则"""
    __tablename__ = "schedule_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)               # 规则名称
    enabled = Column(Boolean, default=True)                  # 启用/暂停
    cron_expression = Column(String(50), nullable=False)     # cron 表达式
    period_type = Column(String(20), nullable=False)         # daily/weekly/monthly/quarterly/yearly
    board_scope = Column(String(200), default="all")         # 板块范围
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
