from starlette_admin.fields import BaseField
from fastapi import Request
from typing import Optional, Any
from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
import json


class GeomField(BaseField):
    render_input_template = "starlette_admin/fields/geom_input.html"
    render_view_template = "starlette_admin/fields/geom_view.html"

    def __init__(self, *args, srid=4326, **kwargs):
        super().__init__(*args, **kwargs)
        self.srid = srid

    async def parse_obj(self, request: Request, obj: Any) -> Any:
        """
        Parses the WKTElement from the database object to be used in the template.
        """
        value = getattr(obj, self.name, None)

        if value is None:
            return {"lat": None, "lng": None}
        print(type(to_shape(value)))
        point: Point = to_shape(value)
        result = point.__geo_interface__
        return str(result["coordinates"])

    def process_form_data(self, value: str) -> Optional[WKTElement]:
        """
        Processes the form data (a JSON string `{"lat": ..., "lng": ...}`)
        back into a WKTElement for the database.
        """
        if not value:
            return None
        try:
            coords = json.loads(value)
            if coords.get("lat") is None or coords.get("lon") is None:
                return None

            point_wkt = f"POINT({coords['lon']} {coords['lat']})"
            return WKTElement(point_wkt, srid=self.srid)
        except (json.JSONDecodeError, TypeError):
            return None
