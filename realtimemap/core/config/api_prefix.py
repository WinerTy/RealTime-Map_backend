import secrets
from typing import Optional

from pydantic import BaseModel


class AuthPrefix(BaseModel):
    login_url: str = "api/v1/auth/login"
    reset_password_token_secret: str = secrets.token_hex()
    verification_token_secret: str = secrets.token_hex()
    token_lifetime_seconds: int = 3600
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None

    @property
    def activate_google_auth(self) -> bool:
        if self.google_client_id and self.google_client_secret:
            return True
        return False


class ApiPrefixV1(BaseModel):
    prefix: str = "/api/v1"
    auth: AuthPrefix = AuthPrefix()


class ApiPrefix(BaseModel):
    v1: ApiPrefixV1 = ApiPrefixV1()
