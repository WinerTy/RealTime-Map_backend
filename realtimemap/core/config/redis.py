from pydantic import BaseModel, RedisDsn


class RedisConfig(BaseModel):
    prefix: str = "realtime-map-cache"
    url: RedisDsn
