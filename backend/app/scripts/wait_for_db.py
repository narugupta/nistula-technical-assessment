import asyncio

from sqlalchemy import text

from app.db.database import engine


async def wait_for_db():

    retries = 15

    for attempt in range(retries):

        try:

            async with engine.begin() as conn:

                await conn.execute(
                    text("SELECT 1")
                )

                print(
                    "Database ready"
                )

                return

        except Exception:

            print(
                f"Waiting for database "
                f"({attempt + 1}/{retries})"
            )

            # postgres startup timing is unpredictable sometimes
            await asyncio.sleep(2)

    raise Exception(
        "Database never became available"
    )


if __name__ == "__main__":

    asyncio.run(wait_for_db())