from fastapi import Request
from fastapi.responses import JSONResponse


async def basic_security_checks(
    request: Request,
    call_next
):

    content_length = request.headers.get(
        "content-length"
    )

    if content_length:

        if int(content_length) > 100000:

            return JSONResponse(
                status_code=413,
                content={
                    "detail": (
                        "Payload too large"
                    )
                }
            )

    # malformed payloads can sometimes DOS parsers
    if request.method == "POST":

        content_type = request.headers.get(
            "content-type",
            ""
        )

        if "application/json" not in content_type:

            return JSONResponse(
                status_code=415,
                content={
                    "detail": (
                        "Unsupported content type"
                    )
                }
            )

    return await call_next(request)