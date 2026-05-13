from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,

    # pool_pre_ping avoids stale connections
    # postgres containers sometimes restart during dev
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)