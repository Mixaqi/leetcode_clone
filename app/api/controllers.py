from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_session_storage
from app.auth.service import AuthService
from app.auth.session_storage import SessionStorage
from app.core.db_helper import get_async_psql_session
from app.schemas.auth import CreateUser, UserSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(
    response: Response,
    user_data: CreateUser,
    db: AsyncSession = Depends(get_async_psql_session),
    session_storage: SessionStorage = Depends(get_session_storage),
) -> UserSchema:
    auth_service = AuthService(db=db)

    try:
        user = await auth_service.register_user(user_data=user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    session_id = await session_storage.create_session(user_id=user.id)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )

    return UserSchema.model_validate(user)
