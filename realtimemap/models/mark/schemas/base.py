from datetime import datetime
from typing import Annotated, Optional, List

from fastapi import UploadFile
from pydantic import BaseModel, Field, field_validator

allowed_duration = [12, 24, 36, 48]


class Coordinates(BaseModel):
    """
    Class for add lon/lat coordinates.
    Two fields required!
    """

    longitude: Annotated[float, Field(..., ge=-180, le=180, examples=["63.201907"])]
    latitude: Annotated[float, Field(..., ge=-90, le=90, examples=["75.445675"])]


class CoordinatesOptional(BaseModel):
    """
    Class for add lon/lat coordinates.
    Two fields not required!
    """

    longitude: Annotated[
        Optional[float], Field(None, ge=-180, le=180, examples=["63.201907"])
    ]
    latitude: Annotated[
        Optional[float], Field(None, ge=-90, le=90, examples=["75.445675"])
    ]


class CommonMarkFields(BaseModel):
    """
    Class for common mark fields.

    """

    additional_info: Annotated[
        Optional[str], Field(None, description="Additional information")
    ]
    photo: Annotated[
        Optional[List[UploadFile]], Field(None, description="Photos for mark")
    ]


class BaseMark(BaseModel):
    """
    Class for base mark fields.
    """

    mark_name: Annotated[
        str, Field(..., min_length=1, max_length=128, description="Mark name")
    ]
    start_at: Annotated[
        datetime,
        Field(default=datetime.now(), description="Current date"),
    ]
    duration: Annotated[int, Field(12, description="Duration in hours.")]

    @field_validator("duration")
    def validate_duration(cls, value):
        if value not in allowed_duration:  # TODO maybe ENUM???
            raise ValueError("Duration not supported.")
        return value
