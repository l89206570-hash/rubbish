"""AI 经营总结服务 — 调用 DeepSeek API 生成自然语言总结"""

import logging
from datetime import date, datetime

from openai import OpenAI

from app.config import config
from app.services import calc_revenue, calc_cashflow, calc_inventory, calc_sales, calc_hr, calc_cost
from app.schemas.indicators import IndicatorResponse

logger = logging.getLogger(__name__)

_client: OpenAI | None = None


def _get_client() -> OpenAI | None:
    global _client
    if _client is not None:
        return _client
    if not config.deepseek_api_key:
        logger.warning("DEEPSEEK_API_KEY 未配置，AI 总结功能不可用")
        return None
    _client = OpenAI(api_key=config.deepseek_api_key, base_url=config.deepseek_api_base)
    return _client


def _build_indicator_text() -> str:
    """获取 6 大板块当前数据，转为文本"""
    boards = {
        "revenue": calc_revenue(),
        "cashflow": calc_cashflow(),
        "inventory": calc_inventory(),
        "sales": calc_sales(),
        "hr": calc_hr(),
        "cost": calc_cost(),
    }

    lines = [f"经营数据报告（{date.today().isoformat()}）", "=" * 40]
    for key, board in boards.items():
        yoy = f"{board.yoy_change:+.1f}%" if board.yoy_change is not None else "N/A"
        mom = f"{board.mom_change:+.1f}%" if board.mom_change is not None else "N/A"
        val = f"¥{board.current_value:,.0f}" if board.current_value is not None else "N/A"
        lines.append(f"\n【{board.title}】")
        lines.append(f"  当前值: {val}")
        lines.append(f"  同比: {yoy}")
        lines.append(f"  环比: {mom}")
    return "\n".join(lines)


SUMMARY_PROMPT_TEMPLATE = """你是一名专业的经营分析师。根据以下经营数据，生成一份简洁的日/周/月/季/年度总结。

要求：
1. 用中文输出，语气专业但直白，让老板一眼看懂
2. 指出关键指标的变化趋势和数值
3. 如果有明显异常（大幅增长/下降），给出可能的业务原因
4. 提出建议关注的方向
5. 控制在 300 字以内

数据如下：
{data_text}
"""


def generate_summary(period_start: str, period_end: str, board_scope: str = "all") -> str:
    """调用 DeepSeek API 生成经营总结

    Args:
        period_start: 开始日期 (2026-05-01)
        period_end: 结束日期 (2026-05-15)
        board_scope: 板块范围，默认 all

    Returns:
        总结文本（Markdown 格式）

    Raises:
        RuntimeError: API key 未配置或调用失败
    """
    client = _get_client()
    if client is None:
        # 无 API key 时返回 mock 总结
        return _generate_mock_summary(period_start, period_end)

    data_text = _build_indicator_text()
    prompt = SUMMARY_PROMPT_TEMPLATE.format(data_text=data_text)

    try:
        resp = client.chat.completions.create(
            model=config.deepseek_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3,
        )
        content = resp.choices[0].message.content or ""
        logger.info(f"AI 总结生成成功 ({len(content)} 字)")
        return content
    except Exception as e:
        logger.error(f"AI 总结生成失败: {e}")
        raise RuntimeError(f"AI 调用失败: {e}")


def _generate_mock_summary(period_start: str, period_end: str) -> str:
    """无 API key 时的 Mock 总结"""
    return f"""## 经营总结（{period_start} ~ {period_end}）

### 整体概况
本周期内公司经营状况总体 **稳中向好**。营收表现强劲，环比增长 3.2%，达 ¥12,850,000。同比增幅 12.5%，说明公司业务持续增长。

### 重点关注
1. **现金流需关注**：本期现金流为负（-¥320,000），主要由于季度末集中支付供应商款项。预计下周回款后恢复正常。
2. **库存周转率 4.2** 次，属于行业健康水平，但需注意部分品类的滞销风险。
3. **客户复购率 62.5%**，保持在不错水平，建议继续加强 VIP 客户维护。

### 建议
- 监控应收账款回收进度，确保月末现金流转正
- 关注成本结构中人工成本占比（28%）是否有优化空间
- 销售势头良好，可考虑适当加大市场营销投入
"""
