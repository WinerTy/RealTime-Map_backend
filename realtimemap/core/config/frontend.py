from typing import Optional

from pydantic import BaseModel


class FrontendConfig(BaseModel):
    url: Optional[str] = "http://example.com"

    def get_password_reset_url(self, token: str) -> str:
        return f"{self.url}/password-reset/?token={token}"

    def get_verify_url(self, token: str) -> str:
        return f"{self.url}/verify/?token={token}"