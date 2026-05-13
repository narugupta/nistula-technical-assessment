from fastapi import APIRouter

from sqlalchemy import (
    select,
    func
)

from app.db.database import AsyncSessionLocal

from app.models.escalation import Escalation
from app.models.db_message import DBMessage
from app.models.failed_event import FailedEvent


router = APIRouter(
    prefix="/operations",
    tags=["operations"]
)


@router.get("/escalations")

async def get_escalations():

    async with AsyncSessionLocal() as session:

        query = await session.execute(
            select(Escalation)
        )

        escalations = query.scalars().all()

        return [

            {
                "id": e.id,

                "severity":
                    e.severity,

                "status":
                    e.status,

                "assigned_agent_id":
                    e.assigned_agent_id,

                "sla_deadline":
                    e.sla_deadline
            }

            for e in escalations
        ]


@router.get("/metrics")

async def get_metrics():

    async with AsyncSessionLocal() as session:

        total_messages = await session.scalar(

            select(
                func.count(DBMessage.id)
            )
        )

        total_escalations = await session.scalar(

            select(
                func.count(Escalation.id)
            )
        )

        failed_events = await session.scalar(

            select(
                func.count(FailedEvent.id)
            )
        )

        auto_send_count = await session.scalar(

            select(
                func.count(DBMessage.id)
            )

            .where(
                DBMessage.action ==
                "auto_send"
            )
        )

        return {

            "total_messages":
                total_messages,

            "total_escalations":
                total_escalations,

            "failed_events":
                failed_events,

            "auto_send_count":
                auto_send_count
        }