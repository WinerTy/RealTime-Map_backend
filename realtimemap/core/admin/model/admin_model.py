from datetime import datetime
from typing import Dict, Any

from fastapi import Request
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession
from starlette_admin import ColorField, DateTimeField, FloatField, IntegerField
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin.fields import PasswordField, FileField, HasOne

from core.admin.fields import GeomField
from models import User, Mark


class AdminCategory(ModelView):
    label = "Categories"
    fields = ["id", "category_name", ColorField("color"), "icon", "is_active"]


class AdminMark(ModelView):
    fields = [
        Mark.id,
        GeomField(
            "geom",
            srid=4326,
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        FloatField(
            "longitude", exclude_from_list=True, exclude_from_detail=True, required=True
        ),
        FloatField(
            "latitude", exclude_from_list=True, exclude_from_detail=True, required=True
        ),
        Mark.mark_name,
        HasOne("owner", identity="user", required=True),
        Mark.additional_info,
        HasOne("category", identity="category", required=True),
        IntegerField("duration", min=12, max=48, step=12, required=True),
        DateTimeField("start_at", label="Start at", required=True),
        Mark.photo,
        Mark.is_ended,
    ]
    exclude_fields_from_create = [Mark.is_ended]

    async def before_create(
        self, request: Request, data: Dict[str, Any], obj: Mark
    ) -> None:
        pass

    @staticmethod
    def convert_geom(data: Dict[str, Any]) -> Dict[str, Any]:
        data["geom"] = f"SRID=4326;POINT({data['longitude']} {data['latitude']})"
        del data["longitude"]
        del data["latitude"]
        return data

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors: Dict[str, str] = dict()

        if data["longitude"] < -180 or data["latitude"] > 180:
            errors["longitude"] = "Not valid longitude"

        if data["latitude"] < -90 or data["longitude"] > 180:
            errors["latitude"] = "Not valid latitude"

        if data["start_at"] < datetime.now():
            errors["start_at"] = "Not valid start at"

        if len(errors) > 0:
            raise FormValidationError(errors)

        valid_data = self.convert_geom(data)
        return await super().validate(request, valid_data)

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        try:
            new_data = await self._arrange_data(request, data)
            await self.validate(request, new_data)
            session: AsyncSession = request.state.session
            mark = await self._populate_obj(request, self.model(), new_data)
            mark.geom = new_data["geom"]
            session.add(mark)
            await self.before_create(request, new_data, mark)
            await session.commit()
            await session.refresh(mark)
            await self.after_create(request, mark)
        except Exception as e:
            return self.handle_exception(e)

    async def _populate_obj(
        self,
        request: Request,
        obj: Any,
        data: Dict[str, Any],
        is_edit: bool = False,
    ) -> Any:
        for field in self.get_fields_list(request, request.state.action):
            if field.name in ["longitude", "latitude"]:
                continue
            name, value = field.name, data.get(field.name, None)
            if isinstance(field, FileField):
                value, should_be_deleted = value
                if should_be_deleted:
                    setattr(obj, name, None)
                elif (not field.multiple and value is not None) or (
                    field.multiple and isinstance(value, list) and len(value) > 0
                ):
                    setattr(obj, name, value)
            else:
                setattr(obj, name, value)
        return obj


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


class AdminMarkComment(ModelView):
    # exclude_fields_from_list = ["mark"]
    pass
