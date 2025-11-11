from datetime import datetime
from typing import Annotated, Optional

from pydantic import Field

from .base import Coordinates


class MarkRequestParams(Coordinates):
    radius: Annotated[int, Field(5000, description="Search radius in meters.")]
    srid: Annotated[int, Field(4326, description="SRID")]
    date: Annotated[
        datetime,
        Field(
            default=datetime.now(),
            description="Date for start filtering. Format YYYY-MM-DD HH:MM:SS",
            examples=["2025-10-30"],
        ),
    ]
    duration: Annotated[
        Optional[int], Field(24, description="Search duration in hours.")
    ]
    show_ended: Annotated[Optional[bool], Field(False, description="Show ended.")]
