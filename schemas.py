from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class UserRegister(BaseModel):
    """注册接口的请求体"""

    username: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[A-Za-z0-9_]+$",
        description="登录用户名，只允许字母、数字和下划线"
    )

    password: str = Field(
        min_length=6,
        max_length=128,
        description="登录密码"
    )

    nickname:str = Field(
       min_length=1,
        max_length=50,
        description="对外展示昵称"
    )

class UserResponse(BaseModel):
    """注册成功后返回给前端的用户信息"""

    id: int
    username: str
    nickname: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[A-Za-z0-9_]+$"
    )
    password: str = Field(
        min_length=6,
        max_length=128
    )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"