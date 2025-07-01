from pydantic import BaseModel, computed_field


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    timeout: int = 900
    workers: int = 4
    domains: str = "127.0.0.1"
    main_domain: str = "realtimemap.ru"

    @property
    def bind(self):
        return f"{self.host}:{self.port}"

    @computed_field
    @property
    def base_url(self) -> str:
        return f"https://{self.main_domain}"


