import asyncio

from sqlalchemy.exc import OperationalError

from app.core.logging import logger

from app.db.base import Base
from app.db.database import engine

from app.models.guest import Guest
from app.models.conversation import Conversation
from app.models.db_message import DBMessage
from app.models.message_event import MessageEvent
from app.models.processing_metrics import (
    ProcessingMetrics
)
from app.models.guest_profile import (
    GuestProfile
)
from app.models.channel_identity import (
    ChannelIdentity
)
from app.models.agent import Agent
from app.models.escalation import Escalation
from app.models.failed_event import (
    FailedEvent
)


async def init_db():

    max_retries = 15
    retry_delay = 2

    for attempt in range(max_retries):

        try:

            async with engine.begin() as conn:

                logger.info(
                    "Creating database tables"
                )

                await conn.run_sync(
                    Base.metadata.create_all
                )

                logger.info(
                    "Database initialized successfully"
                )

                return

        except OperationalError:

            logger.warning(
                f"Database not ready yet "
                f"(attempt {attempt + 1}/"
                f"{max_retries})"
            )

            # postgres containers sometimes need extra startup time
            await asyncio.sleep(retry_delay)

    raise Exception(
        "Could not connect to database"
    )