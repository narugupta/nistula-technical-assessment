from app.services.memory_service import (
    get_recent_guest_history
)


async def build_guest_context(
    unified_message
):

    recent_messages = (
        await get_recent_guest_history(
            unified_message.guest_name
        )
    )

    history_context = []

    for msg in recent_messages:

        history_context.append(
            f"""
Previous Message:
{msg.message_text}

Previous AI Reply:
{msg.ai_reply_text}
"""
        )

    return "\n".join(history_context)