from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.analysis_session import AnalysisSession
    from app.models.matching_analysis import MatchingAnalysis


class Message(Base):
    __tablename__ = "message"

    message_id: Mapped[UUID] = mapped_column(
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

    context_analysis_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "matching_analysis.analysis_id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    session: Mapped[AnalysisSession] = relationship(
        "AnalysisSession",
        back_populates="messages",
    )

    context_analysis: Mapped[MatchingAnalysis | None] = relationship(
        "MatchingAnalysis",
        back_populates="context_messages",
    )

    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "sequence_number",
            name="session_sequence",
        ),
        CheckConstraint(
            "sequence_number > 0",
            name="sequence_number",
        ),
        CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="role",
        ),
        CheckConstraint(
            "length(trim(content)) > 0",
            name="content_not_empty",
        ),
        Index(
            "ix_message_context_analysis",
            "context_analysis_id",
        ),
    )