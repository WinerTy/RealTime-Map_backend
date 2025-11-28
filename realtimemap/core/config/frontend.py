from typing import Optional

from pydantic import BaseModel


class FrontendConfig(BaseModel):
    url: Optional[str] = "http://example.com"