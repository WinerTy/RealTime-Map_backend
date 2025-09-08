from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin

from core.admin.auth.provider import AdminAuthProvider
from core.admin.model import (
    AdminCategory,
    AdminUser,
    AdminMark,
)
from core.app.lifespan import ROOT_DIR
from core.config import conf
from database.helper import db_helper
from models import Category, User, Mark


def setup_admin(app: FastAPI) -> None:
    admin = Admin(
        engine=db_helper.engine,
        title="RealTime-Map",
        auth_provider=AdminAuthProvider(),
        middlewares=[
            Middleware(
                SessionMiddleware, secret_key=conf.api.v1.auth.verification_token_secret
            )
        ],
        templates_dir=ROOT_DIR / "templates",
    )
    admin.add_view(AdminCategory(Category))
    admin.add_view(AdminUser(User))
    admin.add_view(AdminMark(Mark))
    # admin.add_view(AdminUsersBans(UsersBan))
    admin.mount_to(app)
