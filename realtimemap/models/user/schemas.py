from typing import Optional

from fastapi import Request
from fastapi_users import schemas
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: Optional[str] = None
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator("avatar", mode="before")
    def convert_photos_url(cls, v, info: ValidationInfo) -> Optional[str]:
        if not info.context or "request" not in info.context:
            return v.path if v else None

        if v is None:
            return None

        request: Optional[Request] = info.context.get("request")
        file_url = str(
            request.url_for("get_file", storage=v.upload_storage, file_id=v.file_id)
        )

        return file_url


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
