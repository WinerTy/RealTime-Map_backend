from typing import Any

from fastapi import Request
from starlette.datastructures import FormData
from starlette_admin import RequestAction
from starlette_admin.fields import BaseField

from utils.geom_serializator import serialization_geom


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
        result = serialization_geom(value)
        return result.coordinates

    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ) -> Any:
        """
        Extracts the value of this field from submitted form data.
        """
        print(form_data.values())
        return form_data.get(self.id)
