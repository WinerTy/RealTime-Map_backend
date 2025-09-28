from fastapi import FastAPI
from starlette_admin import DropDown
from starlette_admin.contrib.sqla import Admin

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
from core.app.lifespan import ROOT_DIR
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


def setup_admin(app: FastAPI) -> None:
    admin = Admin(
        engine=db_helper.engine,
        title="RealTime-Map",
        # auth_provider=AdminAuthProvider(),
        # middlewares=[
        #     Middleware(
        #         SessionMiddleware, secret_key=conf.api.v1.auth.verification_token_secret
        #     )
        # ],
        templates_dir=ROOT_DIR / "templates",
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
