from collections.abc import AsyncGenerator

from redis.asyncio import Redis, from_url
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


async def get_async_psql_session() -> AsyncGenerator[AsyncSession]:
    async with db_helper.session_factory() as session:
        yield session


db_helper = DatabaseHelper(url=settings.get_database_URL, echo=settings.PG_ECHO)


async def get_redis_client() -> AsyncGenerator[Redis]:
    client = from_url(
        settings.redis.get_redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    try:
        yield client
    finally:
        await client.aclose()
