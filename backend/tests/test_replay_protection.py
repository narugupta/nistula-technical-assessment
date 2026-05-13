from app.services.replay_protection_service import (
    generate_request_fingerprint,
    is_replay_attack
)


def test_replay_detection():

    fingerprint = generate_request_fingerprint(
        "whatsapp",
        "Rahul",
        "123",
        "hello"
    )

    first = is_replay_attack(fingerprint)

    second = is_replay_attack(fingerprint)

    assert first is False
    assert second is True