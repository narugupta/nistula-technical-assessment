from app.services.decision_engine import (
    determine_action
)


def test_complaints_always_escalate():

    result = determine_action(
        0.95,
        "complaint"
    )

    assert result == "escalate"


def test_high_confidence_auto_send():

    result = determine_action(
        0.92,
        "general_enquiry"
    )

    assert result == "auto_send"


def test_low_confidence_escalates():

    result = determine_action(
        0.30,
        "general_enquiry"
    )

    assert result == "escalate"