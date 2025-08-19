from typing import List

from pygeohash import encode, get_adjacent


def get_geohash(lat: float, lon: float, precision: int = 5) -> str:
    geohash = encode(lat, lon, precision)
    return geohash


def get_neighbors(geohash: str) -> List[str]:
    left_sector = get_adjacent(geohash, direction="left")
    right_sector = get_adjacent(geohash, direction="right")
    result = [
        get_adjacent(geohash, "top"),
        get_adjacent(geohash, "bottom"),
        left_sector,
        right_sector,
        get_adjacent(left_sector, "top"),
        get_adjacent(left_sector, "bottom"),
        get_adjacent(right_sector, "top"),
        get_adjacent(right_sector, "bottom"),
    ]
    return result
