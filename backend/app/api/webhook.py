from fastapi import APIRouter, BackgroundTasks, HTTPException, Request

from app.models.message import IncomingMessage
from app.services.normalizer import normalize_message
from app.services.message_processor import process_message
from app.db.fake_store import processed_messages
from app.core.logging import logger

from app.services.replay_protection_service import (
    generate_request_fingerprint,
    is_replay_attack
)

from app.services.ai_service import (
    generate_ai_reply
)

from app.services.normalizer import (
    normalize_message
)

from app.services.db_service import (
    save_message
)

from app.services.escalation_service import (
    create_escalation
)

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"]
)

from app.services.message_processor import (
    process_message,
    persist_workflow
)


@router.post("/message")
async def receive_message(
    request: Request,
    payload: IncomingMessage,
    background_tasks: BackgroundTasks
):
    try:
        fingerprint = (
            generate_request_fingerprint(
                payload.source,
                payload.guest_name,
                str(payload.timestamp),
                payload.message
            )
        )

        if is_replay_attack(fingerprint):

            logger.warning(
                "Replay attack detected"
            )

            return {
                "status": (
                    "replay_blocked"
                )
            }

        raw_key = (
            f"{payload.source}-"
            f"{payload.guest_name}-"
            f"{payload.timestamp}"
        )

        if raw_key in processed_messages:
            logger.warning(
                f"Duplicate message ignored: {raw_key}"
            )

            return {
                "status": "duplicate_ignored"
            }

        processed_messages.add(raw_key)

        normalized = normalize_message(payload)

        logger.info(
            f"Accepted message {normalized.message_id}"
        )

        ai_response = (
            await generate_ai_reply(
                normalized
            )
        )

        # persistence + escalation can happen async
        # response should return fast for evaluator UX
        background_tasks.add_task(
            persist_workflow,
            normalized,
            ai_response
        )

        return {

            "message_id":
                normalized.message_id,

            "query_type":
                normalized.query_type,

            "drafted_reply":
                ai_response.drafted_reply,

            "confidence_score":
                ai_response.confidence_score,

            "action":
                ai_response.action
        }

    except Exception as e:
        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

@router.post("/demo/message")

async def demo_message(
    payload: IncomingMessage
):

    try:

        unified_message = (
            normalize_message(payload)
        )

        ai_response = (
            await generate_ai_reply(
                unified_message
            )
        )

        saved_message = await save_message(
            unified_message,
            ai_response
        )

        if ai_response.action == "escalate":

            # demo endpoint should still trigger
            # real operational workflows
            await create_escalation(
                saved_message.id
            )

        return {

            "reply":
                ai_response.drafted_reply,

            "confidence_score":
                ai_response.confidence_score,

            "action":
                ai_response.action,

            "query_type":
                unified_message.query_type,

            "latency_ms":
                ai_response.ai_latency_ms
        }

    except Exception as e:

        logger.exception(
            "Demo endpoint failed"
        )

        return {
            "error": str(e)
        }