from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from geoalchemy2.functions import ST_SetSRID

from services.geo.service import GeoService
from .schemas_request import MarkRequestParams

DEFAULT_RADIUS_METERS: int = 5000


@dataclass(frozen=True)
class MarkFilter:
    latitude: float
    longitude: float

    geohash_neighbors: List[str]

    duration: int
    min_start: datetime
    max_end: datetime

    current_point: ST_SetSRID

    show_ended: bool

    radius: int = DEFAULT_RADIUS_METERS

    @classmethod
    def from_request(
        cls, req: "MarkRequestParams", geo_service: "GeoService"
    ) -> "MarkFilter":
        current_point = geo_service.create_point(req, req.srid)
        geohash = geo_service.get_geohash(req)
        geohash_neighbors = geo_service.get_neighbors(geohash, True)

        min_start = req.date - timedelta(req.duration)
        max_end = req.date + timedelta(req.duration)

        return cls(
            latitude=req.latitude,
            longitude=req.longitude,
            geohash_neighbors=geohash_neighbors,
            duration=req.duration,
            min_start=min_start,
            max_end=max_end,
            current_point=current_point,
            show_ended=req.show_ended,
            radius=req.radius,
        )
