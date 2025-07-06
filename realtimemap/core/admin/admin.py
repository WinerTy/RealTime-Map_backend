from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from core.admin.model import (
    AdminCategory,
    AdminUser,
    AdminMark,
)
from database.helper import db_helper
from models import Category, User, Mark


def setup_admin(app: FastAPI) -> None:
    # Fix статики в адм на хостинге
    admin = Admin(engine=db_helper.engine, title="RealTime-Map")
    admin.add_view(AdminCategory(Category))
    admin.add_view(AdminUser(User))
    admin.add_view(AdminMark(Mark))
    admin.mount_to(app)
