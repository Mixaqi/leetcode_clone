from sqlalchemy import Column, ForeignKey, Integer

from app.models.base import Base


class UserRole(Base):
    __tablename__ = "users_roles"
    user_id = Column(
        "user_id", Integer, ForeignKey("users.id"), nullable=False, primary_key=True
    )
    roles_id = Column(
        "role_id", Integer, ForeignKey("roles.id"), nullable=False, primary_key=True
    )
