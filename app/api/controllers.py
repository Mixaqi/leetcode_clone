from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import hash_password
from app.core.db_helper import get_async_psql_session
from app.models.userBase import UserBase
from app.schemas.auth import CreateUser, UserSchema
from sqlalchemy import select


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: CreateUser,
    response: Response,
    db: AsyncSession = Depends(get_async_psql_session),
) -> UserBase:
    existing_username = await db.scalar(
        select(UserBase).where(UserBase.username == user_data.username)
    )
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = await db.scalar(
        select(UserBase).where(UserBase.email == user_data.email)
    )
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = UserBase(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.hashed_password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user
