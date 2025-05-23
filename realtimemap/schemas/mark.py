from typing import Optional

from geojson_pydantic import Point
from pydantic import BaseModel, Field

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
    additional_info: Optional[str] = None


class CreateMark(BaseMark):
    geom: str
    owner_id: int
    additional_info: Optional[str] = None


class UpdateMark(CreateMark):
    pass


class ReadMark(BaseMark):
    id: int
    geom: Optional[Point] = None
