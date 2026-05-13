import asyncio


async def retry_async(
    func,
    retries=3,
    delay=1,
    *args,
    **kwargs
):

    last_error = None

    for attempt in range(retries):

        try:
            return await func(*args, **kwargs)

        except Exception as e:

            last_error = e

            # external APIs fail randomly sometimes
            await asyncio.sleep(delay)

    raise last_error