from starlette_admin.contrib.sqla import ModelView
from starlette_admin.contrib.sqla.ext.pydantic import ModelView as PydanticView
from models import User, Mark
from .fields import GeomField

from starlette_admin.fields import PhoneField, PasswordField

from fastapi import Request
from starlette_admin.exceptions import FormValidationError
from typing import Dict, Any


class AdminCategory(ModelView):
    pass


class AdminMark(PydanticView):
    fields = [
        Mark.id,
        GeomField(
            "geom",
            srid=4326,
        ),
        Mark.mark_name,
        Mark.owner,
        Mark.additional_info,
        Mark.category,
    ]


class AdminUser(PydanticView):
    fields = [
        User.id,
        PhoneField("phone", label="Phone"),
        PasswordField(
            "hashed_password",
            label="Password",
            exclude_from_detail=True,
            exclude_from_edit=True,
            exclude_from_list=True,
        ),
        User.email,
        User.username,
        User.is_active,
        User.is_superuser,
        User.is_verified,
    ]

    exclude_fields_from_detail = [User.hashed_password]
    exclude_fields_from_edit = [User.hashed_password]
    # exclude_fields_from_create = [User.hashed_password]
    exclude_fields_from_list = [User.hashed_password]

    async def before_create(
        self, request: Request, data: Dict[str, Any], obj: Any
    ) -> None:
        print(data)

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors: Dict[str, str] = dict()
        if data["phone"] is None:
            errors["phone"] = "Phone number must contain only digits."
        if len(errors) > 0:
            raise FormValidationError(errors)
        return await super().validate(request, data)


class AdminMarkComment(ModelView):
    exclude_fields_from_list = ["mark"]
