from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.message import Message
    from app.models.user import User


class AnalysisSession(Base):
    __tablename__ = "analysis_session"

    session_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
        ),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="waiting_offer",
        server_default="waiting_offer",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped[User | None] = relationship(
        "User",
        back_populates="sessions",
    )

    documents: Mapped[list[Document]] = relationship(
        "Document",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    messages: Mapped[list[Message]] = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            """
            status IN (
                'waiting_offer',
                'ready',
                'analyzing',
                'completed',
                'failed'
            )
            """,
            name="status",
        ),
        CheckConstraint(
            "updated_at >= created_at",
            name="dates",
        ),
        Index(
            "ix_analysis_session_user_created_at",
            "user_id",
            "created_at",
        ),
    )