from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class LoginBase(Base):
    __tablename__ = "logins"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), on_delete="CASCADE", nullable=False
    )

    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
