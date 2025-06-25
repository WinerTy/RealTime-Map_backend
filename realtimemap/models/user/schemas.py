from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: PhoneNumber
    username: str
    avatar: Optional[str] = None

    @field_validator("avatar", mode="before")
    def convert_photos_url(cls, v) -> Optional[str]:
        if v is None:
            return None
        return v.path


class UserCreate(schemas.BaseUserCreate):
    phone: PhoneNumber
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
