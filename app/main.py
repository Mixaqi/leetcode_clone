from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from fastapi.responses import ORJSONResponse

from app.api import api_router
from app.core.config import settings
from app.core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(RedisBackend(redis), prefix=settings.cache.prefix)
    yield
    await redis.aclose()
    await db_helper.engine.dispose()


app = FastAPI(
    title="LeetCode Clone", lifespan=lifespan, default_response_class=ORJSONResponse
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
