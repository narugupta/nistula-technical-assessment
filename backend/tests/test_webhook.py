from tests.conftest import client


def test_webhook_accepts_valid_payload():

    payload = {
        "source": "whatsapp",
        "guest_name": "Rahul Sharma",
        "message": "Is the villa available?",
        "timestamp": "2026-05-05T10:30:00Z",
        "booking_ref": "NIS-001",
        "property_id": "villa-b1"
    }

    response = client.post(
        "/webhook/message",
        json=payload
    )

    assert response.status_code == 200


def test_invalid_channel_rejected():

    payload = {
        "source": "telegram",
        "guest_name": "Rahul Sharma",
        "message": "Hello",
        "timestamp": "2026-05-05T10:30:00Z",
        "property_id": "villa-b1"
    }

    response = client.post(
        "/webhook/message",
        json=payload
    )

    assert response.status_code == 422