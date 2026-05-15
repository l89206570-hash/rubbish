"""销售与客户分析指标计算"""

from app.core.erp_client import MOCK_DASHBOARD_DATA as mock
from app.schemas.indicators import IndicatorResponse, TrendPoint


def calculate(period: str = "current") -> IndicatorResponse:
    data = mock["sales"]
    return IndicatorResponse(
        board="sales",
        title="销售与客户分析",
        current_value=data["current_value"],
        previous_value=data["previous_value"],
        yoy_change=data["yoy_change"],
        mom_change=data["mom_change"],
        trend=[TrendPoint(**p) for p in data["trend"]],
        unit="元",
        extra={
            "customer_count": data["customer_count"],
            "repeat_rate": data["repeat_rate"],
        },
    )
