from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, field_validator

from utils.url_generator import generate_full_image_url


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: Optional[str] = None
    username: str
    avatar: Optional[str] = None

    _validate_avatar = field_validator("avatar", mode="before")(generate_full_image_url)

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
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
