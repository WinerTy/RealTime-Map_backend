from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .api_prefix import ApiPrefix
from .celery import CeleryConfig
from .database import DatabaseConfig
from .logging import LoggingConfig
from .redis import RedisConfig
from .server import ServerConfig


class AppConfig(BaseSettings):
    db: DatabaseConfig
    redis: RedisConfig
    celery: CeleryConfig
    server: ServerConfig = ServerConfig()
    api: ApiPrefix = ApiPrefix()
    static: Path = Path("static")
    log: LoggingConfig = LoggingConfig()
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


conf = AppConfig()  # noqa
