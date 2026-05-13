from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    Float,
    Boolean,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class DBMessage(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    message_id: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    tenant_id: Mapped[str] = mapped_column(String(100))

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id")
    )

    guest_name: Mapped[str] = mapped_column(String(255))

    message_text: Mapped[str] = mapped_column(String)

    query_type: Mapped[str] = mapped_column(String(100))

    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    ai_generated: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

        # whether human staff modified
    # AI draft before sending
    agent_edited: Mapped[bool] = mapped_column(
        default=False
    )

    # tracks operational delivery path
    # examples:
    # ai_auto_send
    # agent_review
    # escalated
    sent_via: Mapped[str] = mapped_column(
        String(50),
        default="agent_review"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # if AI keeps retrying failed events blindly,
    # we can accidentally spam guests later
    processing_status: Mapped[str] = mapped_column(
        String(100),
        default="pending"
    )

    ai_reply_text: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )
    
    action: Mapped[str] = mapped_column(
        String(100),
        default="agent_review"
    )