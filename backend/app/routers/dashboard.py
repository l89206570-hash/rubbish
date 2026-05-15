"""仪表盘数据 API — 6大板块查询接口"""

import logging

from fastapi import APIRouter, Query

from app.services import (
    calc_revenue,
    calc_cashflow,
    calc_inventory,
    calc_sales,
    calc_hr,
    calc_cost,
)
from app.schemas.indicators import IndicatorResponse, DashboardSummary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

BOARD_MAP = {
    "revenue": ("营收利润总览", calc_revenue),
    "cashflow": ("现金流监控", calc_cashflow),
    "inventory": ("库存与供应链", calc_inventory),
    "sales": ("销售与客户分析", calc_sales),
    "hr": ("人效与人力", calc_hr),
    "cost": ("成本结构分析", calc_cost),
}


@router.get("/{board}", response_model=IndicatorResponse)
def get_board(board: str, period: str = Query("current", description="时间范围")):
    """获取单个板块指标数据"""
    if board not in BOARD_MAP:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"未知板块: {board}")

    _, calc_fn = BOARD_MAP[board]
    return calc_fn(period)


@router.get("", response_model=DashboardSummary)
def get_all_boards(period: str = Query("current", description="时间范围")):
    """获取所有6大板块指标数据"""
    return DashboardSummary(
        revenue=calc_revenue(period),
        cashflow=calc_cashflow(period),
        inventory=calc_inventory(period),
        sales=calc_sales(period),
        hr=calc_hr(period),
        cost=calc_cost(period),
    )
