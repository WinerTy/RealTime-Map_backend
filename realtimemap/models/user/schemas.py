from typing import Optional

from fastapi import Request
from fastapi_users import schemas
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: PhoneNumber
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator("avatar", mode="before")
    def convert_photos_url(cls, v, info: ValidationInfo) -> Optional[str]:
        if not info.context or "request" not in info.context:
            # Если контекста нет, мы не можем создать полный URL.
            # Возвращаем просто путь или None.
            return v.path if v else None
        request: Optional[Request] = info.context.get("request")
        base_url = request.url.scheme + "://" + request.url.netloc + "/media/"
        if v is None or request is None:
            return None

        return f"{base_url}{v.path}"


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
