"""营收利润指标计算"""

from app.core.erp_client import MOCK_DASHBOARD_DATA as mock
from app.schemas.indicators import IndicatorResponse, TrendPoint


def calculate(period: str = "current") -> IndicatorResponse:
    data = mock["revenue"]
    return IndicatorResponse(
        board="revenue",
        title="营收利润总览",
        current_value=data["current_value"],
        previous_value=data["previous_value"],
        yoy_change=data["yoy_change"],
        mom_change=data["mom_change"],
        trend=[TrendPoint(**p) for p in data["trend"]],
        unit="元",
    )
