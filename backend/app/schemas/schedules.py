"""调度规则 Schema"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    name: str
    cron_expression: str
    period_type: str
    board_scope: str = "all"


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    cron_expression: Optional[str] = None
    period_type: Optional[str] = None
    board_scope: Optional[str] = None
    enabled: Optional[bool] = None


class ScheduleResponse(BaseModel):
    id: int
    name: str
    enabled: bool
    cron_expression: str
    period_type: str
    board_scope: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
