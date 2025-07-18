from datetime import datetime
from typing import Dict, Any

from starlette.requests import Request
from starlette_admin import (
    HasOne,
    IntegerField,
    DateTimeField,
)
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

from core.admin.fields import GeomField
from models import Mark


class AdminMark(ModelView):
    fields = [
        Mark.id,
        GeomField("geom", srid=4326, required=True),
        Mark.mark_name,
        HasOne("owner", identity="user", required=True),
        Mark.additional_info,
        HasOne("category", identity="category", required=True),
        IntegerField("duration", min=12, max=48, step=12, required=True),
        DateTimeField("start_at", label="Start at", required=True),
        DateTimeField(
            "end_at", label="End at", exclude_from_create=True, exclude_from_edit=True
        ),
        Mark.photo,
        Mark.is_ended,
    ]
    exclude_fields_from_create = [Mark.is_ended]

    async def before_create(
        self, request: Request, data: Dict[str, Any], obj: Mark
    ) -> None:
        pass

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors: Dict[str, str] = dict()

        if data["geom"] is None:
            errors["geom"] = "Geom required. Example: 180,90"

        if request.state.action != "EDIT":
            if data["start_at"] < datetime.now():
                errors["start_at"] = "Start at is before current time"

        if data["owner"] is None:
            errors["owner"] = "Not valid owner"

        if data["category"] is None:
            errors["category"] = "Not valid category"

        if len(errors) > 0:
            raise FormValidationError(errors)

        return await super().validate(request, data)
