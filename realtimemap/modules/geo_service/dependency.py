from functools import lru_cache

from .service import GeoService


@lru_cache(typed=True)
def get_geo_service() -> "GeoService":
    return GeoService()
