from datetime import datetime

from sqlalchemy import (
    String,
    Float,
    DateTime
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class ProcessingMetrics(Base):
    __tablename__ = "processing_metrics"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    message_id: Mapped[str] = mapped_column(
        String(255)
    )

    processing_time_ms: Mapped[float] = mapped_column(
        Float
    )

    ai_latency_ms: Mapped[float] = mapped_column(
        Float
    )

    action: Mapped[str] = mapped_column(
    )