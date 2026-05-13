from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional


class IncomingMessage(BaseModel):
    source: Literal[
        "whatsapp",
        "booking_com",
        "airbnb",
        "instagram",
        "direct"
    ]

    guest_name: str = Field(..., min_length=2)
    message: str = Field(..., min_length=1)
    timestamp: datetime

    booking_ref: Optional[str] = None
    property_id: str


class UnifiedMessage(BaseModel):
    message_id: str
    source: str
    guest_name: str
    message_text: str
    timestamp: datetime
    booking_ref: Optional[str]
    property_id: str
    query_type: str