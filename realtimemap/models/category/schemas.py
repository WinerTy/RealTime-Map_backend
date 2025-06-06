from typing import Any

from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.color import Color


class BaseCategory(BaseModel):
    category_name: str = Field(..., max_length=64)


class CreateCategory(BaseCategory):
    color: str
    icon: UploadFile

    @field_validator("color", mode="before")
    @classmethod
    def validate_and_convert_color_to_hex(cls, v: Any) -> str:
        try:
            color_obj = Color(v)
            return color_obj.as_hex()
        except ValueError as e:
            raise ValueError(f"Invalid color value: '{v}'") from e


class UpdateCategory(CreateCategory):
    pass


class ReadCategory(BaseCategory):
    id: int
    icon: str
    color: str

    @field_validator("icon", mode="before")
    @classmethod
    def generate_url(cls, v: Any):
        try:
            return v.path
        except AttributeError:
            return v
