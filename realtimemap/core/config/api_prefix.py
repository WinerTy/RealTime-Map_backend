import secrets

from pydantic import BaseModel


class AuthPrefix(BaseModel):
    login_url: str = "/auth/login"
    reset_password_token_secret: str = secrets.token_hex()
    verification_token_secret: str = secrets.token_hex()


class ApiPrefixV1(BaseModel):
    prefix: str = "v1"
    auth: AuthPrefix = AuthPrefix()


class ApiPrefix(BaseModel):
    v1: ApiPrefixV1 = ApiPrefixV1()
