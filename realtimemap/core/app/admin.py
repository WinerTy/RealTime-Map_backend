from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from database.helper import db_helper
from models import Category, User, MarkComment, Mark
from models.user.schemas import UserCreate
from .admin_model import AdminCategory, AdminUser, AdminMarkComment, AdminMark
from models.mark.schemas import CreateMark


def setup_admin(app: FastAPI) -> None:
    admin = Admin(engine=db_helper.engine, title="RealTime-Map")
    admin.add_view(AdminCategory(Category))
    admin.add_view(AdminMarkComment(MarkComment))
    admin.add_view(AdminUser(User, pydantic_model=UserCreate))
    admin.add_view(AdminMark(Mark, pydantic_model=CreateMark))
    admin.mount_to(app)
