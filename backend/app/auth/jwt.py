"""JWT 认证中间件（预留 — 环境变量 AUTH_ENABLED 控制开关）

当前：AUTH_ENABLED=false 时完全跳过认证，所有请求直接通过。
启用后：所有 /api/* 请求需要 Bearer token。"""

import logging
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config import config

logger = logging.getLogger(__name__)

ALGORITHM = config.jwt_algorithm
SECRET = config.jwt_secret
EXPIRE_MINUTES = config.jwt_expire_minutes


def create_token(username: str) -> str:
    """创建 JWT token"""
    payload = {
        "sub": username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """验证 JWT token，返回 payload"""
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """FastAPI 中间件 — 验证所有 /api/* 请求的 JWT token"""

    async def dispatch(self, request: Request, call_next):
        if not config.auth_enabled:
            # 认证未启用，直接通过
            return await call_next(request)

        # 公开路径无需认证
        public_paths = ["/api/health", "/api/auth/login", "/docs", "/openapi.json"]
        if any(request.url.path.startswith(p) for p in public_paths):
            return await call_next(request)

        # 需要 /api/* 的请求携带 token
        if request.url.path.startswith("/api"):
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "缺少认证信息"},
                )
            payload = verify_token(auth.removeprefix("Bearer "))
            if payload is None:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "token 无效或已过期"},
                )
            # 将用户信息注入请求
            request.state.user = payload.get("sub")

        return await call_next(request)
