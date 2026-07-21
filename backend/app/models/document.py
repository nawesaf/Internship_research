from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CHAR,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.analysis_session import AnalysisSession
    from app.models.matching_analysis import MatchingAnalysis


class Document(Base):
    __tablename__ = "document"

    document_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    session_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "analysis_session.session_id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True,
    )

    extracted_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sha256: Mapped[str] = mapped_column(
        CHAR(64),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    session: Mapped[AnalysisSession] = relationship(
        "AnalysisSession",
        back_populates="documents",
    )

    cv: Mapped[CV | None] = relationship(
        "CV",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
    )

    job_offer: Mapped[JobOffer | None] = relationship(
        "JobOffer",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
    )

    __table_args__ = (
        CheckConstraint(
            "length(trim(original_filename)) > 0",
            name="filename_not_empty",
        ),
        CheckConstraint(
            "length(trim(storage_key)) > 0",
            name="storage_key_not_empty",
        ),
        CheckConstraint(
            "mime_type = 'application/pdf'",
            name="mime_type",
        ),
        CheckConstraint(
            "sha256 ~ '^[0-9a-f]{64}$'",
            name="sha256",
        ),
        Index(
            "ix_document_session_created_at",
            "session_id",
            "created_at",
        ),
        Index(
            "ix_document_sha256",
            "sha256",
        ),
    )


class CV(Base):
    __tablename__ = "cv"

    document_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "document.document_id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    document: Mapped[Document] = relationship(
        "Document",
        back_populates="cv",
    )

    analyses: Mapped[list[MatchingAnalysis]] = relationship(
        "MatchingAnalysis",
        back_populates="cv",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class JobOffer(Base):
    __tablename__ = "job_offer"

    document_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "document.document_id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    document: Mapped[Document] = relationship(
        "Document",
        back_populates="job_offer",
    )

    analyses: Mapped[list[MatchingAnalysis]] = relationship(
        "MatchingAnalysis",
        back_populates="job_offer",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )