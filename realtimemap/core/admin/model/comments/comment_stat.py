from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload
from starlette.requests import Request

from core.admin.model.base import BaseModelAdmin
from models import CommentStat


class AdminCommentStat(BaseModelAdmin):
    fields = [
        CommentStat.id,
        CommentStat.comment,
        CommentStat.likes_count,
        CommentStat.dislikes_count,
        CommentStat.total_replies,
    ]

    def can_delete(self, request: Request) -> bool:
        return False

    def can_edit(self, request: Request) -> bool:
        return False

    def can_create(self, request: Request) -> bool:
        return False

    def get_list_query(self, request: Request) -> Select:
        stmt = select(self.model).options(joinedload(CommentStat.comment))
        return stmt
