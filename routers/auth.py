from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.formparsers import FormMessage

from database import get_db
from models import User
from schemas import UserRegister, UserResponse, TokenResponse, UserLogin
from security import hash_password, verify_password, create_access_token

router=APIRouter(
    prefix="/auth",
    tags=["认证"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
        user_in: UserRegister,
        session: AsyncSession = Depends(get_db)
):
    existing_user = await session.scalar(
        select(User).where(User.username==user_in.username)
    )
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )
    user = User(
        username=user_in.username,
        nickname=user_in.nickname,
        password_hash=hash_password(user_in.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login",response_model=TokenResponse)
async def login(
        user_in: UserLogin,
        session: AsyncSession = Depends(get_db)
):

    statement = select(User).where(User.username==user_in.username)
    result = await session.execute(statement)
    user: User | None = result.scalar_one_or_none()

    if user is None or not verify_password(
        user_in.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    access_token = create_access_token(
        user_id=user.id,
        username=user.username
    )
    return TokenResponse(access_token=access_token)