from app.db.database import AsyncSessionLocal

from app.models.processing_metrics import (
    ProcessingMetrics
)


async def save_processing_metrics(
    message_id: str,
    processing_time_ms: float,
    ai_latency_ms: float,
    action: str
):

    async with AsyncSessionLocal() as session:

        metrics = ProcessingMetrics(
            message_id=message_id,
            processing_time_ms=processing_time_ms,
            ai_latency_ms=ai_latency_ms,
            action=action
        )

        session.add(metrics)

        # metrics writes are non-critical
        # don't kill guest workflows because analytics failed
        try:
            await session.commit()

        except Exception:
            await session.rollback()