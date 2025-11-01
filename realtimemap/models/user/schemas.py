from typing import Optional, List

from fastapi import UploadFile
from fastapi_users import schemas
from pydantic import BaseModel, field_validator, ConfigDict

from utils.url_generator import generate_full_image_url


class ReadUserSub(BaseModel):
    id: int
    plan_id: int

    model_config = ConfigDict(from_attributes=True)


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: Optional[str] = None
    username: str
    avatar: Optional[str] = None
    subscriptions: Optional[List["ReadUserSub"]] = None
    _validate_avatar = field_validator("avatar", mode="before")(generate_full_image_url)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    username: str

    @field_validator("password")
    def validate_password(cls, value: str):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        return value


class UserUpdate(schemas.BaseUserUpdate):
    @field_validator("password")
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password

    username: Optional[str] = None
    avatar: Optional[UploadFile] = None


class UserLogin(BaseModel):
    username: str
    password: str
