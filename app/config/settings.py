import os
import json

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppSettings(BaseSettings):
    echo: bool = Field(False)
    debug: bool = Field(False)

    host: str = Field("127.0.0.1")
    port: int = Field(8000)
    reload: bool = Field(True)

    start_url: str
    concurrent_requests: int = Field(5)

    schedule_hour: int = Field(12)
    schedule_minute: int = Field(0)

    dumps_dir: str = "dumps"
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64)"

    cookies: dict = Field(default_factory=lambda: json.loads(os.getenv("APP_COOKIES", "{}")))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="APP_"
    )

    @property
    def dumps_path(self) -> Path:
        base_dir = Path.cwd()
        path = base_dir / self.dumps_dir
        path.mkdir(parents=True, exist_ok=True)
        return path


class DbSettings(BaseSettings):
    host: str = Field("db")
    port: int = Field(5432)
    db: str = Field("postgres")
    user: str = Field("postgres")
    password: str = Field("postgres")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="POSTGRES_"
    )

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    db: DbSettings = Field(default_factory=DbSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
