from typing import Any

from fastapi import Request
from geoalchemy2.shape import to_shape
from shapely.geometry import Point
from starlette.datastructures import FormData
from starlette_admin import RequestAction
from starlette_admin.fields import BaseField


class GeomField(BaseField):
    render_input_template = "starlette_admin/fields/geom_input.html"
    render_view_template = "starlette_admin/fields/geom_view.html"
    input_type = "text"

    def __init__(self, *args, srid=4326, **kwargs):
        super().__init__(*args, **kwargs)
        self.srid = srid

    async def parse_obj(self, request: Request, obj: Any) -> Any:
        """
        Parses the WKTElement from the database object to be used in the template.
        """
        value = getattr(obj, self.name, None)

        if value is None:
            return "Coords not found"
        point: Point = to_shape(value)
        result = point.__geo_interface__
        return str(result["coordinates"])

    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ) -> Any:
        """
        Extracts the value of this field from submitted form data.
        """
        print(form_data.values())
        return form_data.get(self.id)
