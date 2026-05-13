from sqlalchemy import select

from app.models.agent import Agent


async def assign_best_agent(session):

    query = await session.execute(

        select(Agent)

        .where(
            Agent.is_available == True
        )

        .order_by(
            Agent.active_escalations.asc()
        )
    )

    agent = query.scalars().first()

    return agent