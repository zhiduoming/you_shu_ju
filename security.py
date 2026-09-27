from datetime import datetime, timezone, timedelta

from pwdlib import PasswordHash
import jwt

from config import settings

# 配置jwt算法
JWT_ALGORITHM = "HS256"

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """把明文密码转换成不可逆密码哈希"""
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """验证用户输入的明文密码是否与数据库哈希匹配"""
    return password_hasher.verify(password, password_hash)


def create_access_token(user_id: int, username: str) -> str:
   expire_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

   payload = {
       "sub": str(user_id), # subject，当前用户的id，JWT中约定来表示身份主体
       "username": username,
       "exp": expire_at
   }

   # 根据payload、signature和expire_time生成jwt_token
   return jwt.encode(
       payload,
       settings.jwt_secret_key,
       algorithm=JWT_ALGORITHM
   )