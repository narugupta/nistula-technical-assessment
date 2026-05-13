from datetime import datetime

from sqlalchemy import (
    String,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class FailedEvent(Base):
    __tablename__ = "failed_events"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    message_id: Mapped[str] = mapped_column(
        String(255)
    )

    failure_reason: Mapped[str] = mapped_column(
        String
    )

    payload_snapshot: Mapped[str] = mapped_column(
        String
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    retry_status: Mapped[str] = mapped_column(
        String(100),
        default="pending"
    )

    # this table can explode in size if retries loop badly
    retry_attempts: Mapped[int] = mapped_column(
        default=0
    )