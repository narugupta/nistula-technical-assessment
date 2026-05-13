from sqlalchemy import select

from app.db.database import AsyncSessionLocal

from app.models.escalation import Escalation
from app.models.db_message import DBMessage

from app.services.sla_service import (
    calculate_sla_deadline
)

from app.services.routing_service import (
    assign_best_agent
)


def determine_severity(
    query_type: str,
    message_text: str
):

    text = message_text.lower()

    if "refund" in text:
        return "critical"

    if query_type == "complaint":
        return "high"

    if "not working" in text:
        return "high"

    return "medium"


async def create_escalation(
    db_message_id: int
):

    async with AsyncSessionLocal() as session:

        message_query = await session.execute(
            select(DBMessage).where(
                DBMessage.id == db_message_id
            )
        )

        message = message_query.scalar_one()

        severity = determine_severity(
            message.query_type,
            message.message_text
        )

        agent = await assign_best_agent(
            session
        )

        escalation = Escalation(
            message_id=message.id,

            assigned_agent_id=(
                agent.id if agent else None
            ),

            severity=severity,

            escalation_reason=(
                f"AI marked message as {message.action}"
            ),

            sla_deadline=(
                calculate_sla_deadline(
                    severity
                )
            )
        )

        session.add(escalation)

        if agent:
            # load balancing is very naive right now
            agent.active_escalations += 1

        await session.commit()

        return escalation