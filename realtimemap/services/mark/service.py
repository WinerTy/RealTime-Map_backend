from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from fastapi import HTTPException
from fastapi_babel import _

from models import User, Mark
from models.mark.schemas import (
    CreateMarkRequest,
    MarkRequestParams,
    UpdateMarkRequest,
)
from models.mark_comment.schemas import CreateMarkCommentRequest
from services.base import BaseService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from crud.mark import MarkRepository
    from crud.category import CategoryRepository
    from crud.mark_comment.repository import MarkCommentRepository
    from websocket.mark_socket import MarkManager


class MarkService(BaseService):
    def __init__(
        self,
        session: "AsyncSession",
        mark_repo: "MarkRepository",
        category_repo: "CategoryRepository",
        mark_comment_repo: "MarkCommentRepository",
        manager: "MarkManager",
    ):
        super().__init__(session)
        self.mark_repo = mark_repo
        self.category_repo = category_repo
        self.mark_comment_repo = mark_comment_repo
        self.manager = manager

    async def create_mark(self, mark_data: CreateMarkRequest, user: User) -> Mark:
        category_exist = await self.category_repo.exist(mark_data.category_id)
        if not category_exist:
            raise HTTPException(
                status_code=422,
                detail=_(f"Category with id {mark_data.category_id} not found."),
            )
        mark = await self.mark_repo.create_mark(mark_data, user)
        return mark

    async def create_comment(
        self, user: User, data: CreateMarkCommentRequest, mark_id: int
    ):
        return await self.mark_comment_repo.create_comment(user, data, mark_id)

    async def get_comments(self, mark_id: int):
        return await self.mark_comment_repo.get_comment_for_mark(mark_id)

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        return await self.mark_repo.get_by_id(mark_id, join_related=["owner"])

    async def get_marks(self, params: MarkRequestParams):
        return await self.mark_repo.get_marks(params)

    async def _before_update_mark(
        self, mark: Mark, user: User, update_data: UpdateMarkRequest
    ) -> None:
        if update_data.category_id:
            if not await self.category_repo.exist(update_data.category_id):
                raise HTTPException(
                    status_code=404,
                    detail=_(f"Category with id {update_data.category_id} not found."),
                )
        if mark.owner_id != user.id:  # Check record owner
            raise HTTPException(
                status_code=403, detail="You are not the owner of this mark"
            )

        passed_time = datetime.now() - mark.created_at
        if passed_time > timedelta(hours=1):
            raise HTTPException(
                status_code=400, detail="The record update time has expired"
            )

    async def update_mark(
        self, user: User, update_data: UpdateMarkRequest, mark_id: int
    ) -> Mark:
        instance = await self.mark_repo.get_mark_by_id(mark_id)
        await self._before_update_mark(instance, user, update_data)
        return await self.mark_repo.update_mark(instance.id, update_data, user)
