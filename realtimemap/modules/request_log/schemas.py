from typing import Optional

from pydantic import BaseModel


class BaseRequestLog(BaseModel):
    user_id: Optional[int] = None
    method: str
    endpoint: str
    params: Optional[str] = None
    headers: Optional[str] = None
    ip: str
    agent: Optional[str] = None


class CreateRequestLog(BaseRequestLog):
    pass


class ReadRequestLog(BaseRequestLog):
    pass


class UpdateRequestLog(BaseRequestLog):
    pass
