from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.session_storage import SessionStorage
from app.auth.utils import hash_password
from app.models.userBase import UserBase


class AuthService:
    def __init__(self, db: AsyncSession, session_storage: SessionStorage):
        self.db = db
        self.session_storage = session_storage

    async def register(
        self, username: str, email: str, password: str
    ) -> tuple[UserBase, str]:
        result = await self.db.execute(select(UserBase).where(UserBase.email == email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = UserBase(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
            created_at=datetime.now(),
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        session_id = await self.session_storage.create_session(new_user.id)

        return new_user, session_id
