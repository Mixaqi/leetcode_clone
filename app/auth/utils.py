from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roleBase import RoleBase
from app.models.userBase import UserBase
from app.models.users_roles import UserRole
from app.schemas.auth import CreateUser
from sqlalchemy import select


ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against a given Argon2 hash.

    Args:
        password (str): The plain-text password to check.
        hashed (str): The Argon2 hash to verify against.

    Returns:
        bool: True if password matches the hash, False otherwise.
    """
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False


async def create_user(db: AsyncSession, user_data: CreateUser) -> UserBase:

    existing_username = await db.scalar(
        select(UserBase).where(UserBase.username == user_data.username)
    )
    if existing_username:
        raise ValueError("Username already exists")

    existing_email = await db.scalar(
        select(UserBase).where(UserBase.email == user_data.email)
    )
    if existing_email:
        raise ValueError("Email already exists")

    new_user = UserBase(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.hashed_password),
    )
    db.add(new_user)
    await db.flush()

    result = await db.execute(select(RoleBase.id).where(RoleBase.title == "USER"))
    user_role_id = result.scalar_one()

    user_role = UserRole(user_id=new_user.id, roles_id=user_role_id)
    db.add(user_role)

    await db.commit()
    await db.refresh(new_user)
    return new_user
