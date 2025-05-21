from geojson_pydantic import Point
from pydantic import BaseModel, Field


class MarkBase(BaseModel):
    mark_name: str = Field(
        ..., min_length=1, max_length=128, description="Название метки"
    )
    owner_id: int = Field(..., description="ID владельца метки (пользователя)")


class MarkCreate(MarkBase):
    latitude: float = Field(..., ge=-90, le=90, description="Широта (от -90 до 90)")
    longitude: float = Field(
        ..., ge=-180, le=180, description="Долгота (от -180 до 180)"
    )


class MarkRead(MarkBase):
    geom: Point
