from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from app.auth.session_storage import SessionStorage
from app.core.db_helper import get_redis_client


async def get_session_storage(
    redis: Annotated[Redis, Depends(get_redis_client)],
) -> SessionStorage:
    return SessionStorage(redis=redis)
