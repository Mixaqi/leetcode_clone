from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlAlchemyEnum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ProblemDifficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ProblemBase(Base):
    __tablename__ = "problems"

    id: Mapped[int] = mapped_column(primary_key=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    competition_id: Mapped[int] = mapped_column(
        ForeignKey("competitions.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    difficulty: Mapped[ProblemDifficulty] = mapped_column(
        SqlAlchemyEnum(ProblemDifficulty), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
