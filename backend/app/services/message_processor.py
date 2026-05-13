from app.core.logging import logger

from app.models.message import UnifiedMessage

from app.services.ai_service import (
    generate_ai_reply
)

from app.services.db_service import (
    save_message
)

from app.services.event_service import (
    log_message_event
)

from app.services.metrics_service import (
    save_processing_metrics
)

from app.utils.timers import Timer

from app.services.escalation_service import (
    create_escalation
)

from app.services.dead_letter_service import (
    store_failed_event
)


async def process_message(
    message: UnifiedMessage
):

    total_timer = Timer()

    logger.info(
        f"Processing message {message.message_id}"
    )

    try:

        logger.info(
            "Starting AI generation"
        )

        ai_response = await generate_ai_reply(
            message
        )

        logger.info(
            "AI generation completed"
        )

        logger.info(
            f"AI action: {ai_response.action}"
        )

        saved_message = await save_message(
            message,
            ai_response
        )

        await log_message_event(
            saved_message.id,
            "ai_reply_generated"
        )

        if ai_response.action == "escalate":
            escalation = await create_escalation(
                saved_message.id
            )

            logger.info(
                f"Escalation created: {escalation.id}"
            )

            await log_message_event(
                saved_message.id,
                "human_escalation_required"
            )

        processing_time = total_timer.elapsed_ms()

        await save_processing_metrics(
            message.message_id,
            processing_time,

            # getattr prevents crashes if latency field is missing
            getattr(
                ai_response,
                "ai_latency_ms",
                0
            ),

            ai_response.action
        )

        logger.info(
            f"Processing completed in "
            f"{processing_time}ms"
        )

    except Exception as e:

        await store_failed_event(
            message.message_id,
            str(message.model_dump()),
            str(e)
        )

        logger.error(
            f"Message processing failed: {str(e)}"
        )

        # failed background tasks are dangerous because
        # FastAPI won't retry them automatically

async def persist_workflow(
    unified_message,
    ai_response
):

    try:

        saved_message = await save_message(
            unified_message,
            ai_response
        )

        if ai_response.action == "escalate":

            await create_escalation(
                saved_message.id
            )

    except Exception:

        logger.exception(
            "Workflow persistence failed"
        )