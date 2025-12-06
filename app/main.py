from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from app.api import api_router
from app.core.config import settings
from app.core.db_helper import db_helper
from app.auth.session_storage import SessionStorage

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
    )
    app.state.redis = redis

    session_storage = SessionStorage(redis)
    app.state.session_storage = session_storage

    test_user_id = 123
    print("Creating test session...")
    session_id = await session_storage.create_session(test_user_id)
    print(f"Session ID: {session_id}")
    session_id = await session_storage.create_session(test_user_id)

    session_data = await session_storage.get_session(session_id)
    print("Session data fetched from Redis:", session_data)

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
