"""指标标准化 Schema — 所有板块共用统一输出格式"""

from typing import Optional, List

from pydantic import BaseModel


class TrendPoint(BaseModel):
    month: str
    value: float


class IndicatorResponse(BaseModel):
    """6大板块共用的指标响应格式"""
    board: str
    title: str
    current_value: Optional[float] = None
    previous_value: Optional[float] = None
    yoy_change: Optional[float] = None   # 同比增长率(%)
    mom_change: Optional[float] = None   # 环比增长率(%)
    trend: List[TrendPoint] = []
    unit: str = "元"                  # 数值单位
    extra: dict = {}                  # 各板块专用扩展字段


class DashboardSummary(BaseModel):
    """所有板块聚合响应"""
    revenue: IndicatorResponse
    cashflow: IndicatorResponse
    inventory: IndicatorResponse
    sales: IndicatorResponse
    hr: IndicatorResponse
    cost: IndicatorResponse
