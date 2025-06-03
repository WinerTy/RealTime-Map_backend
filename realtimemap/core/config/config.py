from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .api_prefix import ApiPrefix
from .database import DatabaseConfig
from .redis import RedisConfig
from .server import ServerConfig


class AppConfig(BaseSettings):
    server: ServerConfig = ServerConfig()
    db: DatabaseConfig
    redis: RedisConfig
    api: ApiPrefix = ApiPrefix()
    static: Path = Path("static")
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


conf = AppConfig()  # noqa
