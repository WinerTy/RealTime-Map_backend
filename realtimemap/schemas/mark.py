from typing import Optional

from fastapi import UploadFile, Request
from geojson_pydantic import Point
from pydantic import BaseModel, Field, model_validator
from pydantic_core.core_schema import ValidationInfo

from core.config import conf
from models import TypeMark


class BaseMark(BaseModel):
    mark_name: str = Field(
        ..., min_length=1, max_length=128, description="Название метки"
    )
    type_mark: TypeMark


class CreateMarkRequest(BaseMark):
    latitude: float = Field(..., ge=-90, le=90, description="Широта (от -90 до 90)")
    longitude: float = Field(
        ..., ge=-180, le=180, description="Долгота (от -180 до 180)"
    )
    additional_info: Optional[str] = Field(
        default=None, description="Дополнительная информация"
    )
    photo: Optional[UploadFile] = None


class CreateMark(BaseMark):
    geom: str
    owner_id: int
    additional_info: Optional[str] = None
    photo: Optional[str] = None


class UpdateMark(CreateMark):
    pass


class ReadMark(BaseMark):
    id: int
    geom: Optional[Point] = None
    photo: Optional[str] = None

    @model_validator(mode="after")
    def generate_ful_image_path(self, info: ValidationInfo) -> "ReadMark":
        if info.context and "request" in info.context and self.photo:
            request: Request = info.context["request"]
            try:
                self.photo = str(request.url_for(str(conf.static), path=self.photo))
            except Exception:
                self.photo = None
                raise
        return self
