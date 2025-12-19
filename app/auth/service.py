from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.auth.utils import create_user, verify_password
from app.models.loginBase import LoginBase
from app.models.userBase import UserBase
from app.schemas.auth import CreateUser, UserLogin


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: CreateUser) -> UserBase:
        new_user = await create_user(db=self.db, user_data=user_data)

        new_login = LoginBase(user_id=new_user.id, last_login=datetime.now())
        self.db.add(new_login)

        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def authenticate_user(self, login_data: UserLogin) -> UserBase:
        query = select(UserBase).where(UserBase.email == login_data.email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()


        if not user or not verify_password(password=login_data.password, hashed=user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        if not user.is_active:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )
        self.db.add(LoginBase(user_id=user.id, last_login=datetime.now()))
        await self.db.commit()
        return user

