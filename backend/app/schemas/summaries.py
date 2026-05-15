"""AI 总结 Schema"""

from datetime import datetime
from pydantic import BaseModel


class SummaryCreate(BaseModel):
    """手动触发总结"""
    period_type: str = "custom"
    period_start: str
    period_end: str
    board_scope: str = "all"


class SummaryResponse(BaseModel):
    id: int
    content: str
    board_scope: str
    period_type: str
    period_start: str
    period_end: str
    trigger_type: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SummaryListResponse(BaseModel):
    total: int
    items: list[SummaryResponse]
