from datetime import datetime
from enum import Enum
from typing import Optional, List, Annotated

from geojson_pydantic import Point
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    field_serializer,
    ConfigDict,
)

from models.category.schemas import ReadCategory
from models.user.schemas import UserRead
from utils.geom.geom_serializator import serialization_geom
from utils.url_generator import generate_full_image_url
from .base import BaseMark, CommonMarkFields


class AllowedDuration(int, Enum):
    pass


class ActionType(str, Enum):
    CREATE = "marks_created"
    READ = "marks_get"
    UPDATE = "marks_updated"
    DELETE = "marks_deleted"


allowed_duration = [12, 24, 36, 48]


class CreateMark(BaseMark, CommonMarkFields):
    """
    Class for create mark in Database.
    """

    geom: Annotated[str, Field(..., description="Geometry of mark. Point string")]
    owner_id: Annotated[int, Field(..., description="Owner id", ge=1)]
    category_id: Annotated[Optional[int], Field(None, description="Category id")]
    geohash: Annotated[str, Field(..., description="Geohash sector for this mark")]


class UpdateMark(BaseModel):
    """
    Class for update mark in Database.
    """

    mark_name: Annotated[Optional[str], Field(None, description="Mark name")]
    start_at: Annotated[Optional[datetime], Field(None, description="Current date")]
    duration: Annotated[Optional[int], Field(None, description="Duration in hours.")]
    category_id: Annotated[Optional[int], Field(None, description="Category id")]
    geohash: Annotated[
        Optional[str], Field(None, description="Geohash sector for this mark")
    ]


class ReadMark(CommonMarkFields):
    """
    Class for read mark.
    """

    id: Annotated[int, Field(..., description="Mark id")]
    mark_name: Annotated[str, Field(..., description="Mark name")]
    owner_id: Annotated[int, Field(..., description="Owner id")]
    geom: Annotated[Point, Field(..., description="Geometry of mark")]
    photo: Annotated[
        Optional[List[str]], Field(default_factory=list, description="Photos for mark")
    ]
    end_at: Annotated[datetime, Field(..., description="End datetime")]
    is_ended: Annotated[bool, Field(..., description="Is ended?")]
    category: ReadCategory

    _validate_photo = field_validator("photo", mode="before")(generate_full_image_url)
    _validate_geom = field_validator("geom", mode="before")(serialization_geom)

    @field_serializer("end_at")
    def serialize_end_at(self, value: datetime) -> str:
        return value.isoformat()

    model_config = ConfigDict(from_attributes=True)


class DetailMark(ReadMark):
    """
    Class for detail mark. Include User
    """

    owner: UserRead
