from fastapi_users import schemas
from pydantic import BaseModel, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRead(schemas.BaseUser[int]):
    id: int
    phone: PhoneNumber
    username: str


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
