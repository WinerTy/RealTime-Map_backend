from datetime import datetime
from typing import Optional, List, Literal

from fastapi import UploadFile
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from geojson_pydantic import Point
from pydantic import BaseModel, Field, field_validator, field_serializer
from pydantic_core.core_schema import ValidationInfo
from sqlalchemy_file.mutable_list import MutableList
from starlette.requests import Request

from models.user.schemas import UserRead


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


class UpdateMarkRequest(BaseModel):
    mark_name: Optional[str] = Field(
        default=None, min_length=1, max_length=128, description="Название метки"
    )
    start_at: Optional[datetime] = Field(default=None, description="Current date")
    duration: Optional[int] = Field(default=None, description="Duration in hours.")
    latitude: Optional[float] = Field(
        default=None, ge=-90, le=90, description="Широта (от -90 до 90)"
    )
    longitude: Optional[float] = Field(
        default=None, ge=-180, le=180, description="Долгота (от -180 до 180)"
    )
    additional_info: Optional[str] = Field(
        default=None, description="Дополнительная информация"
    )
    photo: Optional[List[UploadFile]] = None
    category_id: Optional[int] = None


class CreateMark(BaseMark):
    geom: str
    owner_id: int
    additional_info: Optional[str] = None
    photo: Optional[List[UploadFile]] = None
    category_id: int


class UpdateMark(CreateMark):
    mark_name: Optional[str] = Field(
        default=None, min_length=1, max_length=128, description="Название метки"
    )
    start_at: Optional[datetime] = Field(default=None, description="Current date")
    duration: Optional[int] = Field(default=None, description="Duration in hours.")
    latitude: Optional[float] = Field(
        default=None, ge=-90, le=90, description="Широта (от -90 до 90)"
    )
    longitude: Optional[float] = Field(
        default=None, ge=-180, le=180, description="Долгота (от -180 до 180)"
    )
    additional_info: Optional[str] = Field(
        default=None, description="Дополнительная информация"
    )
    photo: Optional[List[UploadFile]] = None
    category_id: Optional[int] = None


class ReadMark(BaseMark):
    id: int
    owner_id: int
    geom: Optional[Point] = None
    photo: List[str] = []
    end_at: datetime
    is_ended: bool

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
        from_attributes = True

    @field_serializer("end_at")
    def serialize_end_at(self, value: datetime) -> str:
        return value.isoformat()

    @field_validator("geom", mode="before")
    def convert_geom(cls, v: WKBElement):
        result = to_shape(v)
        return Point(**result.__geo_interface__)

    @field_validator("photo", mode="before")
    def convert_photos_url(cls, v: MutableList, info: ValidationInfo):
        if not info.context or "request" not in info.context:
            if v is None:
                return []
            return [photo.path for photo in v]
        request: Optional[Request] = info.context.get("request")
        base_url = request.url.scheme + "://" + request.url.netloc + "/media/"

        return [base_url + photo.path for photo in v] if v else []


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
