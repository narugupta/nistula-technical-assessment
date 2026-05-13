from sqlalchemy import select

from app.db.database import AsyncSessionLocal

from app.models.db_message import DBMessage


async def get_recent_guest_history(
    guest_name: str,
    limit: int = 5
):

    async with AsyncSessionLocal() as session:

        query = await session.execute(

            select(DBMessage)

            .where(
                DBMessage.guest_name == guest_name
            )

            .order_by(
                DBMessage.created_at.desc()
            )

            .limit(limit)
        )

        messages = query.scalars().all()

        return messages