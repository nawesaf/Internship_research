from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document import CV, JobOffer
    from app.models.message import Message
    from app.models.skill_evaluation import SkillEvaluation


class MatchingAnalysis(Base):
    __tablename__ = "matching_analysis"

    analysis_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    cv_document_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "cv.document_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    offer_document_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "job_offer.document_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    technical_skills_score: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    experience_score: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    projects_score: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    education_score: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    constraints_score: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    prompt_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    cv: Mapped[CV] = relationship(
        "CV",
        back_populates="analyses",
    )

    job_offer: Mapped[JobOffer] = relationship(
        "JobOffer",
        back_populates="analyses",
    )

    skill_evaluations: Mapped[list[SkillEvaluation]] = relationship(
        "SkillEvaluation",
        back_populates="analysis",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    context_messages: Mapped[list[Message]] = relationship(
        "Message",
        back_populates="context_analysis",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            "cv_document_id <> offer_document_id",
            name="different_documents",
        ),
        CheckConstraint(
            "technical_skills_score BETWEEN 0 AND 40",
            name="technical_skills_score",
        ),
        CheckConstraint(
            "experience_score BETWEEN 0 AND 25",
            name="experience_score",
        ),
        CheckConstraint(
            "projects_score BETWEEN 0 AND 15",
            name="projects_score",
        ),
        CheckConstraint(
            "education_score BETWEEN 0 AND 10",
            name="education_score",
        ),
        CheckConstraint(
            "constraints_score BETWEEN 0 AND 10",
            name="constraints_score",
        ),
        CheckConstraint(
            "length(trim(explanation)) > 0",
            name="explanation_not_empty",
        ),
        CheckConstraint(
            "length(trim(model_name)) > 0",
            name="model_name_not_empty",
        ),
        CheckConstraint(
            "length(trim(prompt_version)) > 0",
            name="prompt_version_not_empty",
        ),
        Index(
            "ix_matching_analysis_cv",
            "cv_document_id",
        ),
        Index(
            "ix_matching_analysis_offer",
            "offer_document_id",
        ),
        Index(
            "ix_matching_analysis_created_at",
            "created_at",
        ),
    )

    @property
    def total_score(self) -> int:
        return (
            self.technical_skills_score
            + self.experience_score
            + self.projects_score
            + self.education_score
            + self.constraints_score
        )