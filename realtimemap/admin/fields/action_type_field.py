from typing import Any

from starlette.datastructures import FormData
from starlette.requests import Request
from starlette_admin import StringField, RequestAction


class ActionTypeField(StringField):

    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ) -> Any:
        value = form_data.get(self.id)
        if len(value.split(" ")) > 2:
            return value.lower().replace(" ", "_")
        return value.lower()
