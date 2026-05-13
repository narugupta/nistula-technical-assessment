import hashlib
import time


# in-memory for now
# redis would be much safer in distributed systems
REQUEST_CACHE = {}


def generate_request_fingerprint(
    source: str,
    guest_name: str,
    timestamp: str,
    message: str
):

    raw = (
        f"{source}-{guest_name}-"
        f"{timestamp}-{message}"
    )

    return hashlib.sha256(
        raw.encode()
    ).hexdigest()


def is_replay_attack(
    fingerprint: str,
    ttl_seconds: int = 120
):

    now = time.time()

    if fingerprint in REQUEST_CACHE:

        created_at = REQUEST_CACHE[
            fingerprint
        ]

        if now - created_at < ttl_seconds:
            return True

    REQUEST_CACHE[fingerprint] = now

    # this dictionary can grow forever under heavy spam
    # redis expiry would fix this later
    return False