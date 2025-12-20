from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from redis.exceptions import ConnectionError, TimeoutError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_session_storage
from app.auth.service import AuthService
from app.auth.session_storage import SessionStorage
from app.core.db_helper import get_async_psql_session
from app.core.logger import logger
from app.schemas.auth import CreateUser, UserSchema


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserSchema, status_code=201)
async def register(
    response: Response,
    user_data: CreateUser,
    db: Annotated[AsyncSession, Depends(get_async_psql_session)],
    session_storage: Annotated[SessionStorage, Depends(get_session_storage)],
) -> UserSchema:
    auth_service = AuthService(db=db)
    try:
        async with db.begin():
            user = await auth_service.register_user(user_data=user_data)
            session_id = await session_storage.create_session(user_id=user.id)
    except ValueError as e:
        logger.error(e)
        raise HTTPException(status_code=400, detail=str(e)) from e

    except (ConnectionError, TimeoutError) as e:
        logger.error(e)
        raise HTTPException(
            status_code=503,
            detail="Session storage unavailable. Please try again later",
        ) from e
    except SQLAlchemyError as e:
        logger.error(f"Db error during registration: {e}")
        raise HTTPException(
            status_code=503, detail="Database unavailable. Please try again later."
        ) from e

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )

    return UserSchema.model_validate(user)
