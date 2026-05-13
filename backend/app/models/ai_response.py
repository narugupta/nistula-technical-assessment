from pydantic import BaseModel


class AIResponse(BaseModel):
    drafted_reply: str
    confidence_score: float
    action: str
    ai_latency_ms: float = 0.0