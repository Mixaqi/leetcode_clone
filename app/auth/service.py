from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import hash_password
from app.models.userBase import UserBase
from app.models.loginBase import LoginBase

class AuthService:
    def __init__ (self, db: AsyncSession):
        self.db = db

    async def register_user(
        self, username: str, email: str, password: str
    ) -> UserBase:

        new_user = UserBase(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
            created_at=datetime.now(),
        )
        self.db.add(new_user)
        await self.db.flush()

        new_login = LoginBase(user_id=new_user.id, last_login=datetime.now())
        self.db.add(new_login)

        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
