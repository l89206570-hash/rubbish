"""FastAPI 应用入口"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config
from app.core.database import init_local_db
from app.core.erp_client import init_erp_client
from app.routers import dashboard, summaries, schedules
from app.services.scheduler import init_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭生命周期"""
    logger.info("=" * 50)
    logger.info(f"经营驾驶舱 v1.0 启动中...")
    logger.info(f"Mock 模式: {'🟡 开启' if config.mock_mode else '🔴 关闭'}")

    # 初始化本地数据库
    init_local_db()
    logger.info("本地数据库初始化完成 ✓")

    # 初始化 ERP 客户端
    init_erp_client()

    # 初始化调度器（模块4）
    init_scheduler()
    logger.info("APScheduler 调度器初始化完成 ✓")

    logger.info("=" * 50)
    yield
    logger.info("应用关闭")


app = FastAPI(
    title="经营驾驶舱 API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — 允许前端开发服务器跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(dashboard.router)
app.include_router(summaries.router)
app.include_router(schedules.router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "mock_mode": config.mock_mode,
        "erp_connected": not config.mock_mode and bool(config.erp_db_url),
    }
