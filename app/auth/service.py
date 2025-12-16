from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import create_user
from app.models.loginBase import LoginBase
from app.models.userBase import UserBase
from app.schemas.auth import CreateUser


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
