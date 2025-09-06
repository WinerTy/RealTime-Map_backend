import os
from typing import Dict, Any

from fastapi_users.password import PasswordHelper
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette_admin import (
    PasswordField,
    BooleanField,
    row_action,
)
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError, ActionFailed

from core.app.lifespan import ROOT_DIR
from crud.user.repository import UserRepository
from models import User, UsersBan
from models.user_ban.model import BanReason

from models.user_ban.schemas import UserBanCreate

# Пиздец Maybe FIX
template_dir = os.path.join(ROOT_DIR, "templates")
env = Environment(loader=FileSystemLoader(template_dir))


def generate_ban_form():
    template = env.get_template("admin/form/ban_form.html")
    ban_reasons = list(BanReason)
    return template.render(ban_reasons=ban_reasons)


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

    @row_action(
        name="ban_user",
        text="Ban user",
        confirmation="Are you sure you want to ban this user?",
        submit_btn_text="Yes, ban",
        submit_btn_class="btn-success",
        icon_class="fas fa-check-circle",
        form=generate_ban_form(),
    )
    async def ban_user_action(self, request: Request, pk: Any) -> str:
        # Preparate data
        pk = int(pk)
        current_user = self.get_current_user(request)
        self.disable_self_ban(current_user.id, pk)

        # Ban Checking
        session: AsyncSession = request.state.session
        user_repo = UserRepository(session)
        is_banned = await user_repo.user_is_banned(pk)
        if is_banned:
            raise ActionFailed("User already banned")

        # Validate form data
        data: FormData = await request.form()
        valid_data = self.validate_action_form_data(data, pk, current_user.id)

        ban_data = UsersBan(**valid_data.model_dump())
        session.add(ban_data)
        await session.commit()
        await session.refresh(ban_data)
        return f"User was banned: {valid_data.reason}"

    @staticmethod
    def validate_action_form_data(data: FormData, user_id: int, moderator_id: int):
        try:
            full_data = {
                "user_id": user_id,
                "moderator_id": moderator_id,
                "banned_until": data.get("banned_until", None),
                "reason": data.get("reason"),
                "reason_text": data.get("reason_text"),
                "is_permanent": data.get("is_permanent"),
            }
            print(full_data.get("banned_until"))
            valid_data = UserBanCreate(**full_data)
            return valid_data
        except ValueError as e:
            raise ActionFailed(str(e))

    @staticmethod
    def disable_self_ban(current_user_id: int, ban_user_id: int) -> None:
        if current_user_id == ban_user_id:
            raise ActionFailed("Can be ban yourself!")

    @staticmethod
    def get_current_user(request: Request) -> User:
        user: User = request.state.user
        return user if user is not None else None
