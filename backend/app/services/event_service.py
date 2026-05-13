from app.db.database import AsyncSessionLocal

from app.models.message_event import MessageEvent


async def log_message_event(
    db_message_id: int,
    event_type: str
):

    async with AsyncSessionLocal() as session:

        event = MessageEvent(
            message_id=db_message_id,
            event_type=event_type
        )

        session.add(event)

        # events should never crash the main workflow
        try:
            await session.commit()
        except Exception:
            await session.rollback()