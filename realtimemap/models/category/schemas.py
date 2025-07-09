from typing import Any

from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_extra_types.color import Color

from utils.url_generator import generate_full_image_url


class BaseCategory(BaseModel):
    category_name: str = Field(..., max_length=64)


class CreateCategory(BaseCategory):
    color: str
    icon: UploadFile

    @field_validator("color", mode="before")
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
    color: str
    icon: str

    _validate_icon = field_validator("icon", mode="before")(generate_full_image_url)

    model_config = ConfigDict(from_attributes=True)
