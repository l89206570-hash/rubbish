"""调度规则 API — CRUD + 启用/暂停"""

import logging
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_local_db
from app.models.local_models import ScheduleRule
from app.schemas.schedules import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.services.scheduler import add_job_from_rule, remove_job

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/schedules", tags=["schedules"])


@router.post("", response_model=ScheduleResponse)
def create_rule(req: ScheduleCreate, db: Session = Depends(get_local_db)):
    """新增调度规则"""
    rule = ScheduleRule(
        name=req.name,
        cron_expression=req.cron_expression,
        period_type=req.period_type,
        board_scope=req.board_scope,
        enabled=True,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)

    add_job_from_rule(rule)
    return rule


@router.get("", response_model=list[ScheduleResponse])
def list_rules(db: Session = Depends(get_local_db)):
    """列出所有调度规则"""
    return db.query(ScheduleRule).order_by(ScheduleRule.created_at.desc()).all()


@router.get("/{rule_id}", response_model=ScheduleResponse)
def get_rule(rule_id: int, db: Session = Depends(get_local_db)):
    """获取单条规则"""
    rule = db.query(ScheduleRule).filter(ScheduleRule.id == rule_id).first()
    if not rule:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="规则不存在")
    return rule


@router.put("/{rule_id}", response_model=ScheduleResponse)
def update_rule(rule_id: int, req: ScheduleUpdate, db: Session = Depends(get_local_db)):
    """更新调度规则"""
    rule = db.query(ScheduleRule).filter(ScheduleRule.id == rule_id).first()
    if not rule:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="规则不存在")

    update_data = req.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(rule, key, value)
    rule.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(rule)

    # 重新加载调度任务
    remove_job(rule.id)
    if rule.enabled:
        add_job_from_rule(rule)

    return rule


@router.delete("/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_local_db)):
    """删除调度规则"""
    rule = db.query(ScheduleRule).filter(ScheduleRule.id == rule_id).first()
    if not rule:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="规则不存在")

    remove_job(rule.id)
    db.delete(rule)
    db.commit()
    return {"ok": True}
