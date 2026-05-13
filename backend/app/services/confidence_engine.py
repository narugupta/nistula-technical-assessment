def calculate_confidence(
    query_type: str,
    message_text: str,
    ai_reply: str
) -> float:

    score = 0.5

    if len(ai_reply) > 20:
        score += 0.2

    if query_type != "complaint":
        score += 0.15

    if "human team" not in ai_reply.lower():
        score += 0.1

    # vague guest messages are risky to auto-send
    if len(message_text.split()) < 3:
        score -= 0.2

    # complaints should rarely be fully automated
    if query_type == "complaint":
        score -= 0.35

    return max(0.0, min(score, 1.0))