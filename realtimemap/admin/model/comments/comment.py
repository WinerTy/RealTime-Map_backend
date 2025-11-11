from sqlalchemy import Select
from sqlalchemy.orm import joinedload
from starlette.requests import Request

from admin.model.base import BaseModelAdmin
from modules import Comment


class AdminComment(BaseModelAdmin):
    fields = [
        Comment.id,
        Comment.mark,
        Comment.content,
        Comment.parent,
        Comment.owner,
        Comment.stats,
    ]

    exclude_fields_from_create = [Comment.stats]
    exclude_fields_from_edit = [Comment.stats]

    def get_list_query(self, request: Request) -> Select:
        stmt = super().get_list_query(request)
        stmt = stmt.options(
            joinedload(Comment.mark),
            joinedload(Comment.owner),
            joinedload(Comment.stats),
        )
        return stmt
