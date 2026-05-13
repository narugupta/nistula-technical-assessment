from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

from datetime import datetime

from sqlalchemy import DateTime


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)

    tenant_id: Mapped[str] = mapped_column(String(100))

    guest_id: Mapped[int] = mapped_column(
        ForeignKey("guests.id")
    )

    source: Mapped[str] = mapped_column(String(100))

    property_id: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )