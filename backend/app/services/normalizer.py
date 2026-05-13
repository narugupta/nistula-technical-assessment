from app.models.message import IncomingMessage, UnifiedMessage
from app.utils.helpers import generate_message_id


def classify_query(message: str) -> str:

    text = message.lower()

    complaint_keywords = [
        "not working",
        "unhappy",
        "bad",
        "complaint",
        "refund",
        "issue",
        "problem",
        "dirty",
        "broken",
        "poor",
        "disappointed",
        "angry",
        "frustrated",
        "worst"
    ]

    pricing_keywords = [
        "rate",
        "price",
        "cost",
        "pricing"
    ]

    availability_keywords = [
        "available",
        "vacancy",
        "availability"
    ]

    checkin_keywords = [
        "check in",
        "wifi",
        "password"
    ]

    special_request_keywords = [
        "airport",
        "early check",
        "late checkout",
        "decoration"
    ]

    # complaints should get priority classification
    for keyword in complaint_keywords:
        if keyword in text:
            return "complaint"

    for keyword in availability_keywords:
        if keyword in text:
            return "pre_sales_availability"

    for keyword in pricing_keywords:
        if keyword in text:
            return "pre_sales_pricing"

    for keyword in checkin_keywords:
        if keyword in text:
            return "post_sales_checkin"

    for keyword in special_request_keywords:
        if keyword in text:
            return "special_request"

    return "general_enquiry"


def normalize_message(payload: IncomingMessage) -> UnifiedMessage:
    return UnifiedMessage(
        message_id=generate_message_id(),
        source=payload.source,
        guest_name=payload.guest_name,
        message_text=payload.message,
        timestamp=payload.timestamp,
        booking_ref=payload.booking_ref,
        property_id=payload.property_id,
        query_type=classify_query(payload.message)
    )