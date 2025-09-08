from sqlalchemy import Select
from sqlalchemy.orm import selectinload
from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView

from models import UsersBan


class AdminUsersBans(ModelView):
    fields = [UsersBan.user, UsersBan.moderator, UsersBan.banned_at]

    def can_create(self, request: Request) -> bool:
        return False

    def can_edit(self, request: Request) -> bool:
        return False

    def can_delete(self, request: Request) -> bool:
        return False

    def get_list_query(self, request: Request) -> Select:
        q = super().get_list_query(request)

        stmt = q.options(selectinload(UsersBan.user), selectinload(UsersBan.moderator))
        return stmt
