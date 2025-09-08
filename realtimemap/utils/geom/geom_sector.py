from pygeohash import encode


def get_geohash(lat: float, lon: float, precision: int = 5) -> str:
    geohash = encode(lat, lon, precision)
    return geohash
