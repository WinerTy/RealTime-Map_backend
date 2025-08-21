from starlette.datastructures import FormData
from starlette.requests import Request
from starlette_admin import StringField, RequestAction

from utils.geom.geom_sector import get_geohash


class GeoHashField(StringField):
    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ) -> str:
        try:
            lat, lon = form_data.get("geom").split(",")
            geohash = get_geohash(float(lat), float(lon))
            return geohash
        except Exception:
            return ""
