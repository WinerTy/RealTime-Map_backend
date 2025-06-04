from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_extra_types.color import Color


class BaseCategory(BaseModel):
    category_name: str = Field(..., max_length=64)


class CreateCategory(BaseCategory):
    color: str
    icon: str

    @field_validator("color", mode="before")
    @classmethod
    def validate_and_convert_color_to_hex(cls, v: Any) -> str:
        # v - это исходное значение, переданное для поля color
        try:
            # 1. Попытка создать объект Color для валидации
            color_obj = Color(v)
            # 2. Если успешно, конвертируем в HEX
            return color_obj.as_hex()
        except ValueError as e:  # Color может выбросить ValueError при неверном формате
            raise ValueError(f"Invalid color value: '{v}'") from e


class UpdateCategory(CreateCategory):
    pass


class ReadCategory(BaseCategory):
    id: int
    icon: str
    color: str
