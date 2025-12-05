from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class RedisDB(BaseModel):
    cache: int = 0

    model_config = SettingsConfigDict(env_prefix="REDIS_DB_")


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: RedisDB = RedisDB()

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class CacheNamespace(BaseModel):
    sessions: str = "sessions"


class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    PG_NAME: str = ""
    PG_USER: str = ""
    PG_PASSWORD: str = ""
    PG_PORT: int = 5432
    PG_HOST: str = "localhost"
    PG_ECHO: bool = False

    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()

    @property
    def get_database_URL(self) -> str:
        PSQL_ASYNC_LINK = f"postgresql+psycopg_async://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"
        return PSQL_ASYNC_LINK


settings = Settings()
