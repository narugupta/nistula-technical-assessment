import time
import uuid

from fastapi import Request

from app.core.logging import logger


async def add_request_context(request: Request, call_next):

    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    request.state.request_id = request_id

    response = await call_next(request)

    duration_ms = round(
        (time.perf_counter() - start_time) * 1000,
        2
    )

    logger.info(
        f"request_id={request_id} "
        f"path={request.url.path} "
        f"duration_ms={duration_ms}"
    )

    response.headers[
        "X-Request-ID"
    ] = request_id

    return response