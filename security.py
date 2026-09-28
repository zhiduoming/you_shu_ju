from datetime import datetime, timezone, timedelta

from fastapi import security, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models import User

# 配置jwt算法
JWT_ALGORITHM = "HS256"

password_hasher = PasswordHash.recommended()

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """把明文密码转换成不可逆密码哈希"""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """验证用户输入的明文密码是否与数据库哈希匹配"""
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: int, username: str) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),  # subject，当前用户的id，JWT中约定来表示身份主体
        "username": username,
        "exp": expire_at
    }

    # 根据payload、signature和expire_time生成jwt_token
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=JWT_ALGORITHM
    )


async def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
        session: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录已失效，请重新登录",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise credentials_exception

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[JWT_ALGORITHM]
        )
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise credentials_exception
    result = await session.execute(select(User).where(User.id == user_id))
    user: User | None = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user
