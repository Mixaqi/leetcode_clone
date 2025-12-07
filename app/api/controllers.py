from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import get_async_psql_session
from app.models.userBase import UserBase
from app.schemas.auth import CreateUser, UserSchema
from app.auth.utils import create_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(
    user_data: CreateUser, db: AsyncSession = Depends(get_async_psql_session)
) -> UserBase:
    try:
        user = await create_user(db, user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user
