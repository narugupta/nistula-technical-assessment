import time

from fastapi import Request
from fastapi.responses import JSONResponse


RATE_LIMIT_CACHE = {}

MAX_REQUESTS = 10
WINDOW_SECONDS = 60


async def rate_limit_middleware(
    request: Request,
    call_next
):

    client_ip = request.client.host

    now = time.time()

    requests = RATE_LIMIT_CACHE.get(
        client_ip,
        []
    )

    requests = [
        r for r in requests
        if now - r < WINDOW_SECONDS
    ]

    if len(requests) >= MAX_REQUESTS:

        return JSONResponse(
            status_code=429,
            content={
                "detail": (
                    "Rate limit exceeded"
                )
            }
        )

    requests.append(now)

    RATE_LIMIT_CACHE[client_ip] = requests

    # this falls apart if multiple app replicas exist
    # redis would become mandatory then
    return await call_next(request)