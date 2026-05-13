from sqlalchemy import (
    String,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class ChannelIdentity(Base):
    __tablename__ = "channel_identities"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    guest_id: Mapped[int] = mapped_column(
        ForeignKey("guests.id")
    )

    source: Mapped[str] = mapped_column(
        String(100)
    )

    external_user_id: Mapped[str] = mapped_column(
        String(255)
    )