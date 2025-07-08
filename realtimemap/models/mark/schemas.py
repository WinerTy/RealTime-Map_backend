from datetime import datetime
from typing import Optional, List, Literal

from fastapi import UploadFile
from geojson_pydantic import Point
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    field_serializer,
    model_validator,
)

from models.category.schemas import ReadCategory
from models.user.schemas import UserRead
from utils.geom_serializator import serialization_geom
from utils.url_generator import generate_full_image_url

allowed_duration = [12, 24, 36, 48]


class BaseMark(BaseModel):
    mark_name: str = Field(
        ..., min_length=1, max_length=128, description="Название метки"
    )
    start_at: datetime = Field(datetime.now(), description="Current date")
    duration: int = Field(12, description="Duration in hours.")

    @field_validator("duration")
    def validate_duration(cls, value):
        if value not in allowed_duration:
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


class UpdateMarkRequest(BaseModel):
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    mark_name: Optional[str] = None
    start_at: Optional[datetime] = None
    duration: Optional[int] = None
    additional_info: Optional[str] = None
    photo: Optional[List[UploadFile]] = None
    category_id: Optional[int] = None

    @model_validator(mode="after")
    def check_lat_lon_pair(self) -> "UpdateMarkRequest":
        if (self.latitude is not None and self.longitude is None) or (
            self.latitude is None and self.longitude is not None
        ):
            raise ValueError(
                "Both latitude and longitude must be provided together or neither"
            )
        return self


class CreateMark(BaseMark):
    geom: str
    owner_id: int
    additional_info: Optional[str] = None
    photo: Optional[List[UploadFile]] = None
    category_id: int


class UpdateMark(BaseModel):
    mark_name: Optional[str] = None
    start_at: Optional[datetime] = None
    duration: Optional[int] = None
    additional_info: Optional[str] = None
    photo: Optional[List[UploadFile]] = None
    category_id: Optional[int] = None
    geom: Optional[str] = None


class ReadMark(BaseMark):
    id: int
    owner_id: int
    geom: Optional[Point] = None
    photo: Optional[List[str]] = []
    end_at: datetime
    is_ended: bool
    category: ReadCategory
    additional_info: Optional[str] = Field(
        default=None, description="Дополнительная информация"
    )
    _validate_photo = field_validator("photo", mode="before")(generate_full_image_url)
    _validate_geom = field_validator("geom", mode="before")(serialization_geom)

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
        from_attributes = True

    @field_serializer("end_at")
    def serialize_end_at(self, value: datetime) -> str:
        return value.isoformat()


class DetailMark(ReadMark):
    owner: UserRead


class Coordinates(BaseModel):
    longitude: float = Field(..., ge=-180, le=180, examples=["63.201907"])
    latitude: float = Field(..., ge=-90, le=90, examples=["75.445675"])


class MarkRequestParams(Coordinates):
    radius: int = Field(500, description="Search radius in meters.")
    srid: int = Field(4326, description="SRID")
    date: datetime = Field(datetime.now(), description="Date")
    duration: Optional[int] = Field(24, description="Search duration in hours.")
    show_ended: Optional[bool] = Field(False, description="Show ended.")


action_type = Literal["marks_created", "marks_get", "marks_updated", "marks_deleted"]


class MarkResponseWebSocket(BaseModel):
    action_type: action_type
    items: List[ReadMark] = []
