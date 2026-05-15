"""调度规则 Schema"""

from datetime import datetime
from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    name: str
    cron_expression: str
    period_type: str
    board_scope: str = "all"


class ScheduleUpdate(BaseModel):
    name: str | None = None
    cron_expression: str | None = None
    period_type: str | None = None
    board_scope: str | None = None
    enabled: bool | None = None


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
