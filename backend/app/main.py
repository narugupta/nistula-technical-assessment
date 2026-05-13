from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.webhook import router as webhook_router

from app.core.logging import logger
from app.db.init_db import init_db

from app.middleware.request_context import add_request_context
from app.api.operations import (
    router as operations_router
)

from app.services.agent_service import (
    seed_agents
)

from app.middleware.rate_limit import (
    rate_limit_middleware
)

from app.middleware.security import (
    basic_security_checks
)

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating database tables")

    await init_db()
    await seed_agents()

    yield

    logger.info("Shutting down application")


app = FastAPI(
    title="Nistula AI Hospitality Platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(add_request_context)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(basic_security_checks)
app.include_router(health_router)
app.include_router(webhook_router)
app.include_router(operations_router)

logger.info("Nistula backend started")