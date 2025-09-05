from typing import Dict, Any

from fastapi_users.password import PasswordHelper
from sqlalchemy import Select
from sqlalchemy.orm import selectinload, joinedload
from starlette.requests import Request
from starlette_admin import PasswordField, BooleanField
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

from models import User, UsersBan


class AdminUser(ModelView):
    fields = [
        User.id,
        User.username,
        User.email,
        User.phone,
        PasswordField(
            "hashed_password",
            label="Password",
            exclude_from_detail=True,
            exclude_from_edit=True,
            exclude_from_list=True,
            required=True,
        ),
        User.avatar,
        User.is_active,
        User.is_superuser,
        User.is_verified,
        BooleanField(
            "bans",
            label="is_banned",
            read_only=True,
            exclude_from_edit=True,
            exclude_from_create=True,
        ),
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
        data["hashed_password"] = hashed_password

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors: Dict[str, str] = dict()
        if len(errors) > 0:
            raise FormValidationError(errors)
        return await super().validate(request, data)

    def get_list_query(self, request: Request) -> Select:
        return super().get_list_query(request)
