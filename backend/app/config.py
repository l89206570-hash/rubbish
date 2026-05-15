"""应用配置管理 — 从环境变量读取全部配置"""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    # FastAPI
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # 本地数据库（驾驶舱自身数据：调度配置、总结历史、用户等）
    local_db_url: str = os.getenv("LOCAL_DB_URL", "sqlite:///./data/dashboard.db")

    # ERP 数据库连接（只读）
    erp_db_host: str = os.getenv("ERP_DB_HOST", "")
    erp_db_port: int = int(os.getenv("ERP_DB_PORT", "3306"))
    erp_db_user: str = os.getenv("ERP_DB_USER", "")
    erp_db_password: str = os.getenv("ERP_DB_PASSWORD", "")
    erp_db_name: str = os.getenv("ERP_DB_NAME", "")
    erp_db_type: str = os.getenv("ERP_DB_TYPE", "mysql")  # mysql | postgresql

    # DeepSeek API
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_api_base: str = os.getenv(
        "DEEPSEEK_API_BASE", "https://api.deepseek.com"
    )
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # 认证（预留）
    auth_enabled: bool = os.getenv("AUTH_ENABLED", "false").lower() == "true"
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

    # Mock 模式（无真实 ERP 时使用模拟数据）
    mock_mode: bool = os.getenv("MOCK_MODE", "true").lower() == "true"

    @property
    def erp_db_url(self) -> str:
        """构造 ERP 数据库连接字符串"""
        if not self.erp_db_host:
            return ""
        if self.erp_db_type == "mysql":
            return (
                f"mysql+pymysql://{self.erp_db_user}:{self.erp_db_password}"
                f"@{self.erp_db_host}:{self.erp_db_port}/{self.erp_db_name}"
            )
        elif self.erp_db_type == "postgresql":
            return (
                f"postgresql+psycopg2://{self.erp_db_user}:{self.erp_db_password}"
                f"@{self.erp_db_host}:{self.erp_db_port}/{self.erp_db_name}"
            )
        return ""

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent.parent.parent


config = Config()
