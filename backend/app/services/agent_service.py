from sqlalchemy import select

from app.db.database import AsyncSessionLocal

from app.models.agent import Agent


async def seed_agents():

    async with AsyncSessionLocal() as session:

        existing = await session.execute(
            select(Agent)
        )

        if existing.scalars().first():
            return

        agents = [
            Agent(
                agent_name="Priya",
                team="guest_experience"
            ),

            Agent(
                agent_name="Rahul",
                team="operations"
            ),

            Agent(
                agent_name="Ananya",
                team="vip_support"
            )
        ]

        session.add_all(agents)

        # if this fails repeatedly during startup,
        # duplicate agents can pile up later
        await session.commit()