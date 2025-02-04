"""
Main aendpoints file.
"""

from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from back.config import settings
from back.logging import logger
from back.routers import imei_check_router, imei_check_sandbox_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Max requests count."""

    redis_connection: redis.Redis = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        encoding="utf-8",
    )
    await FastAPILimiter.init(redis_connection)
    yield
    await FastAPILimiter.close()
    logger.info("Somefing end.")


app = FastAPI(lifespan=lifespan)

app.include_router(imei_check_router, prefix="/api")
app.include_router(imei_check_sandbox_router, prefix="/api")
