from pydantic import BaseModel


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    timeout: int = 900
    workers: int = 4
    domains: str = "127.0.0.1"


    @property
    def bind(self):
        return f"{self.host}:{self.port}"




