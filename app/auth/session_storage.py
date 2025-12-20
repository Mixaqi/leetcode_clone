import json
import uuid
from datetime import UTC, datetime

from redis.asyncio import Redis

from app.schemas.auth import SessionData


class SessionStorage:
    def __init__(self, redis: Redis, ttl_days: int = 7) -> None:
        self.redis: Redis = redis
        self.ttl_seconds: int = ttl_days * 24 * 60 * 60

    async def create_session(self, user_id: int) -> str:
        session_id = str(uuid.uuid4())
        json_data = SessionData(
            user_id=user_id, created_at=datetime.now(UTC)
        ).model_dump_json()
        await self.redis.setex(f"session:{session_id}", self.ttl_seconds, json_data)
        return session_id

    async def get_session(self, session_id: str) -> SessionData | None:
        raw = await self.redis.get(f"session:{session_id}")
        if not raw:
            return None
        data = json.loads(raw)
        return SessionData.model_validate(data)

    async def delete_session(self, session_id: str) -> None:
        await self.redis.delete(f"session:{session_id}")
