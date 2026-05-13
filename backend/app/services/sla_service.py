from datetime import (
    datetime,
    timedelta
)


def calculate_sla_deadline(
    severity: str
):

    now = datetime.utcnow()

    if severity == "critical":
        return now + timedelta(minutes=10)

    if severity == "high":
        return now + timedelta(minutes=30)

    if severity == "medium":
        return now + timedelta(hours=2)

    return now + timedelta(hours=6)