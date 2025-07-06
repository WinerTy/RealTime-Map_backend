from pydantic import BaseModel


class CeleryConfig(BaseModel):
    broker: str
    backend: str
