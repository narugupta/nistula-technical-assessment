from app.db.database import AsyncSessionLocal

from app.models.failed_event import (
    FailedEvent
)


async def store_failed_event(
    message_id: str,
    payload_snapshot: str,
    failure_reason: str
):

    async with AsyncSessionLocal() as session:

        failed_event = FailedEvent(
            message_id=message_id,
            payload_snapshot=payload_snapshot,
            failure_reason=failure_reason
        )

        session.add(failed_event)

        # losing failed events makes debugging horrible later
        await session.commit()