import json
from dataclasses import dataclass
from typing import Any

from starlette.datastructures import FormData
from starlette.requests import Request
from starlette_admin import RequestAction, BaseField


@dataclass
class JsonField(BaseField):
    form_template: str = "forms/json_form.html"
    type: str = "json"

    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ) -> Any:
        try:
            value = form_data.get(self.id)
            return json.loads(value) if value is not None else None  # type: ignore
        except json.JSONDecodeError:
            return None
