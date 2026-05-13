from app.services.confidence_engine import (
    calculate_confidence
)


def test_complaint_confidence_low():

    score = calculate_confidence(
        "complaint",
        "The AC is broken",
        "We are checking with the team"
    )

    assert score < 0.6


def test_simple_query_confidence_high():

    score = calculate_confidence(
        "general_enquiry",
        "Wifi password?",
        "The wifi password is Nistula@2024"
    )

    assert score > 0.7