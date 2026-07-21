from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    String,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.matching_analysis import MatchingAnalysis


class SkillEvaluation(Base):
    __tablename__ = "skill_evaluation"

    analysis_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "matching_analysis.analysis_id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    skill_name: Mapped[str] = mapped_column(
        String(150),
        primary_key=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    analysis: Mapped[MatchingAnalysis] = relationship(
        "MatchingAnalysis",
        back_populates="skill_evaluations",
    )

    __table_args__ = (
        CheckConstraint(
            "length(trim(skill_name)) > 0",
            name="skill_name_not_empty",
        ),
        CheckConstraint(
            "status IN ('matched', 'missing')",
            name="status",
        ),
        Index(
            "ix_skill_evaluation_analysis_status",
            "analysis_id",
            "status",
        ),
    )