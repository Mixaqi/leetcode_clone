from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from app.api import api_router
from app.auth.session_storage import SessionStorage
from app.core.config import settings
from app.core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
    )
    app.state.redis = redis

    session_storage = SessionStorage(redis)
    app.state.session_storage = session_storage
    yield
    await redis.close()
    await redis.connection_pool.disconnect()
    await db_helper.engine.dispose()


app = FastAPI(
    title="LeetCode Clone", lifespan=lifespan, default_response_class=ORJSONResponse
)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
