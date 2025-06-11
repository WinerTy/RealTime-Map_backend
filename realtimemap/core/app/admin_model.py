from starlette_admin.contrib.sqla import ModelView
from starlette_admin.contrib.sqla.ext.pydantic import ModelView as PydanticView

from models import User


class AdminCategory(ModelView):
    pass


class AdminMark(ModelView):
    pass


class AdminUser(PydanticView):
    # fields = [User.email]

    # exclude_fields_from_detail = [User.hashed_password]
    exclude_fields_from_edit = [User.hashed_password]
    # exclude_fields_from_create = [User.hashed_password]
    exclude_fields_from_list = [User.hashed_password]
