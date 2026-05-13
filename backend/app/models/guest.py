from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(primary_key=True)

    # keeping tenant_id from day 1 makes SaaS migration easier later
    tenant_id: Mapped[str] = mapped_column(String(100))

    guest_name: Mapped[str] = mapped_column(String(255))

    # this may break later if multiple guests share same name
    # eventually we should use phone/email identity resolution
    external_guest_ref: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )