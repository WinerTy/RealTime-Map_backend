from typing import Dict, Any

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette_admin.exceptions import FormValidationError

from admin.model.base import BaseModelAdmin
from models import CommentReaction


# TODO Придумать как ограничить в админке
class AdminCommentReaction(BaseModelAdmin):
    fields = [
        CommentReaction.user,
        CommentReaction.comment,
        CommentReaction.reaction_type,
        CommentReaction.created_at,
    ]

    exclude_fields_from_create = [CommentReaction.created_at]

    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        try:
            result = await super().create(request, data)
            return result
        except (IntegrityError, UniqueViolationError):
            raise FormValidationError(
                {"user": "User reaction at this comment already exists."}
            )
