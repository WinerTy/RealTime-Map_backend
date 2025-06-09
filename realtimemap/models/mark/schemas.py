from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile
from geojson_pydantic import Point
from pydantic import BaseModel, Field, field_validator
from sqlalchemy_file.mutable_list import MutableList


class BaseMark(BaseModel):
    mark_name: str = Field(
        ..., min_length=1, max_length=128, description="Название метки"
    )
    start_at: datetime = Field(datetime.now(), description="Current date")
    duration: int = Field(12, description="Duration in hours.")

    @field_validator("duration")
    def validate_duration(cls, value):
        if value not in [12, 24, 48]:
            raise ValueError("Duration not supported.")
        return value


class CreateMarkRequest(BaseMark):
    latitude: float = Field(..., ge=-90, le=90, description="Широта (от -90 до 90)")
    longitude: float = Field(
        ..., ge=-180, le=180, description="Долгота (от -180 до 180)"
    )
    additional_info: Optional[str] = Field(
        default=None, description="Дополнительная информация"
    )
    photo: Optional[List[UploadFile]] = None
    category_id: int


class CreateMark(BaseMark):
    geom: str
    owner_id: int
    additional_info: Optional[str] = None
    photo: Optional[List[UploadFile]] = None
    category_id: int


class UpdateMark(CreateMark):
    pass


class ReadMark(BaseMark):
    id: int
    geom: Optional[Point] = None
    photo: List[str] = []
    end_at: datetime
    is_ended: bool

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }

    @field_validator("photo", mode="before")
    @classmethod
    def convert_photos_url(cls, v: MutableList):
        if v is None:
            return []
        result: List[str] = []

        for photo in v:
            result.append(photo.path)

        return result


class MarkCoordinates(BaseModel):
    longitude: float = Field(..., ge=-180, le=180, examples=["63.201907"])
    latitude: float = Field(..., ge=-90, le=90, examples=["75.445675"])


class MarkRequestParams(MarkCoordinates):
    radius: int = Field(500, description="Search radius in meters.")
    srid: int = Field(4326, description="SRID")
    date: datetime = Field(datetime.now(), description="Date")
    duration: Optional[int] = Field(24, description="Search duration in hours.")
    show_ended: Optional[bool] = Field(False, description="Show ended.")
