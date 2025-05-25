from fastapi_users import schemas
from pydantic import BaseModel, field_validator


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: str
    username: str


class UserCreate(schemas.BaseUserCreate):
    phone: str
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    @field_validator("password")
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password


class UserLogin(BaseModel):
    username: str
    password: str
