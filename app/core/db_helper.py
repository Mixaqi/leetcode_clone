from typing import AsyncGenerator

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


async def get_async_psql_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_helper.session_factory() as session:
        yield session


class RedisHelper:
    def __init__(self, url: str) -> None:
        self.url = url

    async def get_redis_client(self) -> AsyncGenerator[Redis, None]:
        client = Redis.from_url(self.url, encoding="utf-8", decode_responses=True)
        try:
            yield client
        finally:
            await client.aclose()


redis_helper = RedisHelper(url=settings.redis.get_redis_url)
db_helper = DatabaseHelper(url=settings.get_database_URL, echo=settings.PG_ECHO)
