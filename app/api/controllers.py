from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import AuthService
from app.core.db_helper import get_async_psql_session
from app.schemas.auth import CreateUser, UserSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(
    user_data: CreateUser,
    db: AsyncSession = Depends(get_async_psql_session),
) -> UserSchema:
    auth_service = AuthService(db=db)

    try:
        user = await auth_service.register_user(user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserSchema.model_validate(user)
