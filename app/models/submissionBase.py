from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SubmissionBase(Base):
    __tablename__ = "submissions"
    id: Mapped[int] = mapped_column(primary_key=True)

    competition_id: Mapped[int] = mapped_column(
        ForeignKey("competitions.id"), nullable=False
    )
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    test_case_results: Mapped[JSONB] = mapped_column(
        JSONB, nullable=False, server_default="[]"
    )
    is_passed: Mapped[bool] = mapped_column(default=False, nullable=False)
    error: Mapped[str] = mapped_column(Text, nullable=True)
    runtime_ms: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
