import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parents[2] / ".env", encoding="utf-8")


def _env(key: str, default: str | None = None) -> str | None:
    value = os.environ.get(key)
    if value:
        return value
    return default


class Settings(BaseModel):
    project_name: str = "KajovoMail Backend"
    environment: str = "local"
    debug: bool = False

    database_url: str
    redis_url: str
    secret_key: str = "changeme"
    openai_api_key: str | None = None

    artifact_dir: Path = Path("./artifacts")

    class Config:
        extra = "ignore"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


def get_settings() -> Settings:
    return Settings(
        database_url=_env("DATABASE_URL", "postgresql+asyncpg://kajovo:secret@localhost:5432/kajovo"),
        redis_url=_env("REDIS_URL", "redis://localhost:6379/0"),
        secret_key=_env("SECRET_KEY", "change-me"),
        openai_api_key=_env("OPENAI_API_KEY"),
    )
