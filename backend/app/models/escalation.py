from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class Escalation(Base):
    __tablename__ = "escalations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id")
    )

    assigned_agent_id: Mapped[int | None] = mapped_column(
        ForeignKey("agents.id"),
        nullable=True
    )

    severity: Mapped[str] = mapped_column(
        String(50)
    )

    escalation_reason: Mapped[str] = mapped_column(
        String(255)
    )

    status: Mapped[str] = mapped_column(
        String(100),
        default="open"
    )

    sla_deadline: Mapped[datetime] = mapped_column(
        DateTime
    )

    resolved: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # this can get messy later if agents manually reassign tickets a lot
    escalation_notes: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )