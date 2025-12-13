from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.userBase import UserBase
from app.models.loginBase import LoginBase
from app.schemas.auth import CreateUser
from app.auth.utils import create_user


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: CreateUser) -> UserBase:
        new_user = await create_user(db=self.db, user_data=user_data)
        self.db.add(new_user)
        await self.db.flush()

        new_login = LoginBase(user_id=new_user.id, last_login=datetime.now())
        self.db.add(new_login)

        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
