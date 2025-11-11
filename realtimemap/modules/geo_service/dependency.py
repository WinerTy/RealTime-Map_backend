from .service import GeoService


async def get_geo_service() -> GeoService:
    yield GeoService()
