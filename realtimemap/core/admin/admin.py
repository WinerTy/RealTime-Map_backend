from typing import Optional

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette_admin import DropDown
from starlette_admin.contrib.sqla import Admin

from core.admin.auth.provider import AdminAuthProvider
from core.admin.model import (
    AdminCategory,
    AdminUser,
    AdminMark,
    AdminComment,
    AdminCommentStat,
    AdminUsersBans,
    AdminCommentReaction,
    AdminSubscriptionPlan,
    AdminUserSubscription,
)
from core.admin.view.home import HomeView
from core.config import conf
from database.helper import db_helper
from models import (
    Category,
    User,
    Mark,
    Comment,
    CommentStat,
    UsersBan,
    CommentReaction,
    SubscriptionPlan,
    UserSubscription,
)
from utils import format_key


class RealTimeMapAdmin(Admin):
    def _setup_templates(self) -> None:
        super()._setup_templates()
        self.templates.env.filters["format_key"] = format_key

    def custom_render_js(self, request: Request) -> Optional[str]:
        pass


def setup_admin(app: FastAPI) -> None:
    admin = RealTimeMapAdmin(
        engine=db_helper.engine,
        title="RealTime-Map",
        index_view=HomeView(label="Home", icon="fa fa-home"),
        auth_provider=AdminAuthProvider(),
        middlewares=[
            Middleware(
                SessionMiddleware, secret_key=conf.api.v1.auth.verification_token_secret
            )
        ],
        statics_dir=conf.static_dir / "admin",
        templates_dir=conf.template_dir / "admin",
    )
    admin.add_view(
        DropDown(
            "Users",
            icon="fa fa-list",
            views=[
                AdminUser(User),
                AdminUsersBans(UsersBan),
            ],
        )
    )
    admin.add_view(
        DropDown(
            label="Subs",
            icon="fa fa-list",
            views=[
                AdminSubscriptionPlan(SubscriptionPlan),
                AdminUserSubscription(UserSubscription),
            ],
        ),
    )
    admin.add_view(AdminCategory(Category))
    admin.add_view(AdminMark(Mark))
    admin.add_view(
        DropDown(
            "Comments",
            icon="fa fa-list",
            views=[
                AdminComment(Comment),
                AdminCommentStat(CommentStat),
                AdminCommentReaction(CommentReaction),
            ],
        )
    )
    admin.mount_to(app)
