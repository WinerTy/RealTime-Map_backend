from pydantic import BaseModel


class HTTPErrorDetail(BaseModel):
    detail: str
