"""认证路由（预留）"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth.jwt import create_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(req: LoginRequest):
    """登录接口（预留 — 当前直接返回 token）"""
    # TODO: 接入用户数据库验证密码
    if not req.username or not req.password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")

    token = create_token(req.username)
    return {"access_token": token, "token_type": "bearer"}
