from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    PG_NAME: str = "leetcode_db"
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "password"
    PG_PORT: int = 5432
    PG_HOST: str = "localhost"

    @property
    def get_database_URL(self) -> str:
        return f"postgresql+psycopg_async://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"


settings = Settings()

print(settings.get_database_URL)