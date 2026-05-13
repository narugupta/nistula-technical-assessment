from anthropic import AsyncAnthropic

from app.core.config import settings
from app.core.logging import logger

from app.prompts.hospitality_prompt import build_prompt

from app.utils.timers import Timer

from app.services.confidence_engine import (
    calculate_confidence
)

from app.services.decision_engine import (
    determine_action
)

from app.prompts.enriched_prompt import (
    build_enriched_prompt
)

from app.services.context_builder import (
    build_guest_context
)

from app.models.ai_response import AIResponse


client = AsyncAnthropic(
    api_key=settings.ANTHROPIC_API_KEY
)


async def generate_ai_reply(unified_message):
    timer = Timer()

    guest_context = (
        await build_guest_context(
            unified_message
        )
    )

    prompt = build_enriched_prompt(
        guest_name=unified_message.guest_name,
        message=unified_message.message_text,
        query_type=unified_message.query_type,
        guest_context=guest_context
    )

    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            temperature=0.3,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        ai_reply = response.content[0].text

        confidence = calculate_confidence(
            unified_message.query_type,
            unified_message.message_text,
            ai_reply
        )

        action = determine_action(
            confidence,
            unified_message.query_type
        )
        ai_latency_ms = timer.elapsed_ms()

        return AIResponse(
        drafted_reply=ai_reply,
        confidence_score=confidence,
        action=action,
        ai_latency_ms=ai_latency_ms
        )

    except Exception as e:

        logger.error(
            f"Claude API failure: {str(e)}"
        )

        # if Anthropic goes down,
        # we still need graceful guest handling
        fallback_reply = (
            "Thank you for your message. "
            "Our hospitality team will assist you shortly."
        )

        return AIResponse(
            drafted_reply=fallback_reply,
            confidence_score=0.4,
            action="agent_review"
        )