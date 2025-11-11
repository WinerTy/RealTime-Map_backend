from __future__ import annotations

from typing import List

from geoalchemy2 import Geometry
from geoalchemy2.functions import (
    ST_SetSRID,
    ST_MakePoint,
    ST_DistanceSphere,
)
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Latitude, Longitude
from pygeohash import encode, get_adjacent, decode

from modules import Mark
from modules.mark.schemas import Coordinates


class GeoService:
    """
    Service class for work with GEOMETRY
    """

    @staticmethod
    def create_point(coords: "Coordinates", srid: int = 4326):
        """Method for create sql expression"""
        return ST_SetSRID(ST_MakePoint(coords.longitude, coords.latitude), srid)

    @staticmethod
    def create_geometry_point(coords: "Coordinates", srid: int = 4326) -> str:
        return f"SRID={srid};POINT({coords.longitude} {coords.latitude})"

    @staticmethod
    def get_geohash(coords: "Coordinates", precision: int = 5) -> str:
        """Method for get geohash from sql expression"""
        return encode(coords.latitude, coords.longitude, precision=precision)

    @staticmethod
    def get_coords(geohash: str) -> Coordinates:
        result = decode(geohash)
        return Coordinates(
            latitude=Latitude(result.latitude), longitude=Longitude(result.longitude)
        )

    @staticmethod
    def get_neighbors(geohash: str, need_include: bool = False) -> List[str]:
        """Method for get neighbors from geohash"""
        left_sector = get_adjacent(geohash, direction="left")
        right_sector = get_adjacent(geohash, direction="right")
        result = [
            get_adjacent(geohash, "top"),
            get_adjacent(geohash, "bottom"),
            left_sector,
            get_adjacent(left_sector, "top"),
            get_adjacent(left_sector, "bottom"),
            right_sector,
            get_adjacent(right_sector, "top"),
            get_adjacent(right_sector, "bottom"),
        ]
        if need_include:
            result.append(geohash)
        return result

    @staticmethod
    def distance_sphere(geom_1: Geometry, geom_2: Geometry, radius: int = 500):
        return ST_DistanceSphere(geom_1, geom_2, radius)

    @staticmethod
    def create_coordinates(data: BaseModel) -> Coordinates:
        if hasattr(data, "latitude") and hasattr(data, "longitude"):
            return Coordinates(latitude=data.latitude, longitude=data.longitude)
        raise ValueError("Data object must have 'latitude' and 'longitude' attributes")

    def check_geohash_proximity(self, coords: "Coordinates", mark: Mark) -> bool:
        geohash = self.get_geohash(coords)
        neighbors = self.get_neighbors(geohash, need_include=True)

        if mark.geohash in neighbors:
            return True
        return False
