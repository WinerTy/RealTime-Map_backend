from starlette_admin.contrib.sqla import ModelView
from starlette_admin.contrib.sqla.ext.pydantic import ModelView as PydanticView

from models import User
from .fields import GeomField


class AdminCategory(ModelView):
    pass


class AdminMark(PydanticView):
    fields = [
        "id",
        GeomField(
            "geom",
            srid=4326,
        ),
    ]


class AdminUser(PydanticView):
    # fields = [User.email]

    # exclude_fields_from_detail = [User.hashed_password]
    exclude_fields_from_edit = [User.hashed_password]
    # exclude_fields_from_create = [User.hashed_password]
    exclude_fields_from_list = [User.hashed_password]


class AdminMarkComment(ModelView):
    exclude_fields_from_list = ["mark"]
