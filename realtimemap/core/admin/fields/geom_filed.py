import logging
from typing import Any

from fastapi import Request
from starlette.datastructures import FormData
from starlette_admin import RequestAction
from starlette_admin.fields import StringField

from utils.geom_serializator import serialization_geom

logger = logging.getLogger(__name__)


class GeomField(StringField):

    def __init__(self, *args, srid=4326, **kwargs):
        super().__init__(*args, **kwargs)
        self.srid = srid

    async def parse_obj(self, request: Request, obj: Any) -> str:
        """
        Parses the WKTElement from the database object to be used in the template.
        """
        value = getattr(obj, self.name, None)
        if value is None:
            return "Coords not found"
        result = serialization_geom(value)
        coords = result.coordinates._asdict()

        return f"{coords.get("latitude")}, {coords.get("longitude")}"

    @staticmethod
    def _validate_coords(data: str) -> str:
        try:
            lat, lon = data.split(",")

            lat = float(lat)
            lon = float(lon)

            if lat < -90 or lat > 90:
                raise ValueError

            if lon < -180 or lon > 180:
                raise ValueError
            return f"SRID=4326;POINT({lon} {lat})"

        except Exception:
            raise

    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ) -> Any:
        """
        Extracts the value of this field from submitted form data.
        """
        try:
            geom = form_data.get(self.id)
            wkb_coords = self._validate_coords(geom)
            return wkb_coords
        except Exception as e:
            logger.warning(f"Failed to parse value in {self.id}. {str(e)}")
            return None
