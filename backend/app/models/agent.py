from sqlalchemy import (
    String,
    Boolean
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    agent_name: Mapped[str] = mapped_column(
        String(255)
    )

    team: Mapped[str] = mapped_column(
        String(100)
    )

    is_available: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    active_escalations: Mapped[int] = mapped_column(
        default=0
    )