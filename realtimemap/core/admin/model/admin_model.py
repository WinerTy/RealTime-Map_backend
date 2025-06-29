from typing import Dict, Any

from fastapi import Request
from fastapi_users.password import PasswordHelper
from starlette_admin import ColorField, StringField
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.contrib.sqla.ext.pydantic import ModelView as PydanticView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import PhoneField, PasswordField

from core.admin.fields import GeomField
from models import User, Mark


class AdminCategory(ModelView):
    label = "Categories"
    fields = ["id", "category_name", ColorField("color"), "icon", "is_active"]


class AdminMark(PydanticView):
    fields = [
        Mark.id,
        GeomField(
            "geom",
            srid=4326,
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        StringField("longitude", exclude_from_list=True, exclude_from_detail=True),
        StringField("latitude", exclude_from_list=True, exclude_from_detail=True),
        Mark.mark_name,
        Mark.owner,
        Mark.additional_info,
        Mark.category,
        Mark.duration,
        Mark.start_at,
        Mark.is_ended,
    ]


class AdminUser(ModelView):
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
        User.avatar,
    ]

    exclude_fields_from_detail = [User.hashed_password]
    exclude_fields_from_edit = [User.hashed_password]
    # exclude_fields_from_create = [User.hashed_password]
    exclude_fields_from_list = [User.hashed_password]

    async def before_create(
        self, request: Request, data: Dict[str, Any], obj: Any
    ) -> None:
        helper = PasswordHelper()
        user_password = data["hashed_password"]
        hashed_password = helper.hash(password=user_password)
        print(hashed_password)
        data["hashed_password"] = hashed_password

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors: Dict[str, str] = dict()
        print(data["phone"])
        if len(errors) > 0:
            raise FormValidationError(errors)
        return await super().validate(request, data)


class AdminMarkComment(ModelView):
    # exclude_fields_from_list = ["mark"]
    pass
