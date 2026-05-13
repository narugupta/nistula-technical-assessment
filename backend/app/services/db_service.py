from sqlalchemy import select

from app.db.database import AsyncSessionLocal

from app.models.guest import Guest
from app.models.conversation import Conversation
from app.models.db_message import DBMessage
from app.models.message_event import MessageEvent

from app.services.guest_service import (
    get_or_create_guest_profile,
    register_channel_identity
)


async def save_message(
    unified_message,
    ai_response=None
):

    async with AsyncSessionLocal() as session:

        # guest names are not globally unique
        # prefixing with source avoids obvious collisions
        external_guest_ref = (
            f"{unified_message.source}:"
            f"{unified_message.guest_name}"
        )

        guest_query = await session.execute(

            select(Guest)

            .where(
                Guest.external_guest_ref ==
                external_guest_ref
            )
        )

        guest = (
            guest_query
            .scalar_one_or_none()
        )

        if not guest:

            guest = Guest(

                tenant_id="nistula",

                guest_name=
                    unified_message.guest_name,

                external_guest_ref=
                    external_guest_ref
            )

            session.add(guest)

            await session.flush()

        await get_or_create_guest_profile(

            session,

            guest.id,

            unified_message.source
        )

        # real systems would use platform-specific
        # external user IDs instead of names
        await register_channel_identity(

            session,

            guest.id,

            unified_message.source,

            unified_message.guest_name
        )

        # conversations should behave like threads
        # reuse latest matching conversation if possible
        conversation_query = await session.execute(

            select(Conversation)

            .where(
                Conversation.guest_id == guest.id,

                Conversation.source ==
                    unified_message.source,

                Conversation.property_id ==
                    unified_message.property_id
            )

            .order_by(
                Conversation.created_at.desc()
            )
        )

        conversation = (
            conversation_query
            .scalars()
            .first()
        )

        if not conversation:

            conversation = Conversation(

                tenant_id="nistula",

                guest_id=guest.id,

                source=
                    unified_message.source,

                property_id=
                    unified_message.property_id
            )

            session.add(conversation)

            await session.flush()

        message = DBMessage(

            message_id=
                unified_message.message_id,

            tenant_id="nistula",

            conversation_id=
                conversation.id,

            guest_name=
                unified_message.guest_name,

            message_text=
                unified_message.message_text,

            query_type=
                unified_message.query_type,

            confidence_score=(

                ai_response.confidence_score

                if ai_response
                else 0.0
            ),

            ai_generated=bool(ai_response),

            # assessment explicitly asks
            # for workflow tracking
            agent_edited=False,

            sent_via=(

                "ai_auto_send"

                if ai_response
                and ai_response.action == "auto_send"

                else ai_response.action

                if ai_response

                else "agent_review"
            ),

            ai_reply_text=(

                ai_response.drafted_reply

                if ai_response
                else None
            ),

            action=(

                ai_response.action

                if ai_response
                else "agent_review"
            )
        )

        session.add(message)

        await session.flush()

        event = MessageEvent(

            message_id=message.id,

            event_type="message_received"
        )

        session.add(event)

        # if commit fails midway,
        # postgres rollback protects partial writes
        await session.commit()

        return message