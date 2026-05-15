"""定时调度管理 — APScheduler 集成

支持：
- 动态添加/移除/暂停调度任务
- 从 SQLite 持久化规则恢复调度
- 每个调度任务触发 AI 总结生成 + 持久化"""

import logging
from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from app.config import config
from app.core.database import LocalSessionLocal
from app.models.local_models import SummaryRecord, ScheduleRule

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def _run_summary_job(rule_id: int, period_type: str, period_start: str, period_end: str, board_scope: str):
    """调度任务执行体：生成总结并保存到数据库"""
    from app.services.ai_summary import generate_summary

    logger.info(f"⏰ 调度任务触发: {period_type} ({period_start} ~ {period_end})")

    try:
        content = generate_summary(period_start, period_end, board_scope)
    except Exception as e:
        logger.error(f"调度总结生成失败: {e}")
        return

    db = LocalSessionLocal()
    try:
        record = SummaryRecord(
            content=content,
            board_scope=board_scope,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            trigger_type="auto",
        )
        db.add(record)
        db.commit()
        logger.info(f"调度总结已保存 (id={record.id})")
    except Exception as e:
        logger.error(f"保存调度总结失败: {e}")
        db.rollback()
    finally:
        db.close()


def _calc_period(period_type: str) -> tuple[str, str]:
    """根据周期类型计算起止日期"""
    today = date.today()
    if period_type == "daily":
        return today.isoformat(), today.isoformat()
    elif period_type == "weekly":
        start = today.__class__.fromordinal(today.toordinal() - today.weekday())
        return start.isoformat(), today.isoformat()
    elif period_type == "monthly":
        start = today.replace(day=1)
        return start.isoformat(), today.isoformat()
    elif period_type == "quarterly":
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        start = today.replace(month=quarter_start_month, day=1)
        return start.isoformat(), today.isoformat()
    elif period_type == "yearly":
        start = today.replace(month=1, day=1)
        return start.isoformat(), today.isoformat()
    return today.isoformat(), today.isoformat()


def add_job_from_rule(rule: ScheduleRule):
    """根据调度规则添加 APScheduler 任务"""
    start, end = _calc_period(rule.period_type)

    scheduler.add_job(
        id=f"rule_{rule.id}",
        func=_run_summary_job,
        trigger=CronTrigger.from_crontab(rule.cron_expression),
        args=[rule.id, rule.period_type, start, end, rule.board_scope],
        replace_existing=True,
        misfire_grace_time=300,
    )
    logger.info(f"调度任务已添加: {rule.name} ({rule.cron_expression})")


def remove_job(rule_id: int):
    """移除调度任务"""
    job_id = f"rule_{rule_id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        logger.info(f"调度任务已移除: rule_{rule_id}")


def restore_scheduler():
    """应用启动时恢复所有启用的调度规则"""
    db = LocalSessionLocal()
    try:
        rules = db.query(ScheduleRule).filter(ScheduleRule.enabled == True).all()  # noqa: E712
        for rule in rules:
            add_job_from_rule(rule)
        logger.info(f"已恢复 {len(rules)} 条调度规则")
    finally:
        db.close()


def init_scheduler():
    """初始化调度器"""
    jobstores = {
        "default": SQLAlchemyJobStore(url=config.local_db_url),
    } if "sqlite" in config.local_db_url else {}

    scheduler.configure(jobstores=jobstores or None)
    scheduler.start()
    restore_scheduler()
    logger.info("APScheduler 已启动")
