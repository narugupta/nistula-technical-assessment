from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class GuestProfile(Base):
    __tablename__ = "guest_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    guest_id: Mapped[int] = mapped_column(
        unique=True
    )

    total_conversations: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    total_messages: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    preferred_channel: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # storing preferences as text for now keeps schema flexible
    # this will probably evolve into jsonb later
    guest_preferences: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )