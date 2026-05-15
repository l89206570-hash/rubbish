"""AI 总结 API — 生成 + 查询历史"""

import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_local_db
from app.models.local_models import SummaryRecord
from app.schemas.summaries import SummaryCreate, SummaryResponse, SummaryListResponse
from app.services.ai_summary import generate_summary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/summaries", tags=["summaries"])


@router.post("/generate", response_model=SummaryResponse)
def create_summary(req: SummaryCreate, db: Session = Depends(get_local_db)):
    """手动触发 AI 总结生成"""
    try:
        content = generate_summary(req.period_start, req.period_end, req.board_scope)
    except RuntimeError as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=502, detail=str(e))

    record = SummaryRecord(
        content=content,
        board_scope=req.board_scope,
        period_type=req.period_type,
        period_start=req.period_start,
        period_end=req.period_end,
        trigger_type="manual",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@router.get("", response_model=SummaryListResponse)
def list_summaries(
    period_type: Optional[str] = Query(None),
    trigger_type: Optional[str] = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_local_db),
):
    """查询总结历史列表"""
    q = db.query(SummaryRecord).order_by(SummaryRecord.created_at.desc())

    if period_type:
        q = q.filter(SummaryRecord.period_type == period_type)
    if trigger_type:
        q = q.filter(SummaryRecord.trigger_type == trigger_type)

    total = q.count()
    items = q.offset(offset).limit(limit).all()

    return SummaryListResponse(total=total, items=items)


@router.get("/{summary_id}", response_model=SummaryResponse)
def get_summary(summary_id: int, db: Session = Depends(get_local_db)):
    """获取单条总结详情"""
    record = db.query(SummaryRecord).filter(SummaryRecord.id == summary_id).first()
    if not record:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="总结不存在")
    return record
