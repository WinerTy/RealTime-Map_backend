from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from .api_prefix import ApiPrefix
from .celery import CeleryConfig
from .database import DatabaseConfig
from .logging import LoggingConfig
from .payment import YooKassaPayment
from .redis import RedisConfig
from .server import ServerConfig
from .socket import SocketIOConfig

ROOT_DIR = Path(__file__).parent.parent.parent

class AppConfig(BaseSettings):
    db: DatabaseConfig
    redis: RedisConfig
    celery: CeleryConfig
    server: ServerConfig = ServerConfig()
    socket: SocketIOConfig
    api: ApiPrefix = ApiPrefix()
    static: Path = Path("static")
    root_dir: Path = ROOT_DIR

    log: LoggingConfig = LoggingConfig()
    payment: YooKassaPayment
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore"
    )

    @property
    def template_dir(self) -> Path:
        return self.root_dir / "templates"


conf = AppConfig()  # noqa