from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.loginBase import LoginBase
from app.models.roleBase import RoleBase
from app.models.userBase import UserBase
from app.models.users_roles import UserRole


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def _get_role_id_by_title(self, title: str) -> int:
        query = select(RoleBase.id).where(RoleBase.title == title)
        result = await self.db_session.execute(query)
        return result.scalar_one()

    async def get_user_by_email_or_username(
        self, email: str, username: str
    ) -> UserBase | None:
        query = select(UserBase).where(
            (UserBase.email == email) | (UserBase.username == username)
        )
        return await self.db_session.scalar(query)

    async def assign_role_to_user(self, user_id: int, role_title: str) -> None:
        role_id = await self._get_role_id_by_title(role_title)
        user_role = UserRole(user_id=user_id, roles_id=role_id)
        self.db_session.add(user_role)

    async def create_user(self, user: UserBase) -> UserBase:
        self.db_session.add(user)
        await self.db_session.flush()
        return user

    async def add_user_role(self, user_id: int, role_id: int) -> None:
        user_role = UserRole(user_id=user_id, roles_id=role_id)
        self.db_session.add(user_role)

    async def log_login(self, user_id: int) -> None:
        login_entry = LoginBase(user_id=user_id, last_login=datetime.now())
        self.db_session.add(login_entry)
