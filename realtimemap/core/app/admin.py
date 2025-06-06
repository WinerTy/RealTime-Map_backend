from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from database.helper import db_helper
from models import Category
from .admin_model import AdminCategory


def setup_admin(app: FastAPI) -> None:
    admin = Admin(engine=db_helper.engine, title="RealTime-Map")
    admin.add_view(AdminCategory(Category))
    admin.mount_to(app)
