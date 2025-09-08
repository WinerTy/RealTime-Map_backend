from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from crud.category import CategoryRepository
from exceptions import RecordNotFoundError, UserPermissionError, TimeOutError
from models import User, Mark
from models.mark.schemas import (
    CreateMarkRequest,
    MarkRequestParams,
    UpdateMarkRequest,
)
from services.base import BaseService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from websocket.mark_socket import MarkManager
    from crud.mark import MarkRepository
    from crud.mark_comment import MarkCommentRepository


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
            raise RecordNotFoundError()
        mark = await self.mark_repo.create_mark(mark_data, user)
        return mark

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        result = await self.mark_repo.get_by_id(
            mark_id, join_related=["owner", "category"]
        )
        if not result:
            raise RecordNotFoundError()
        return result

    async def get_marks(self, params: MarkRequestParams):
        result = await self.mark_repo.get_marks(params)
        return result

    async def _before_update_mark(
        self, mark_id: int, user: User, update_data: UpdateMarkRequest
    ) -> Mark:
        """
        The method is called before updating
        1. Checks the existence of the selected category
        2.Checking the existence of a post and the author of the post
        3. Checking for editing timeout
        If additional checks are needed, add below
        """
        await self._check_category_exist(update_data.category_id)
        mark = await self._check_mark_ownership(mark_id, user)
        self._check_timeout(mark)
        return mark

    async def update_mark(
        self, user: User, update_data: UpdateMarkRequest, mark_id: int
    ) -> Mark:
        mark = await self._before_update_mark(mark_id, user, update_data)
        return await self.mark_repo.update_mark(mark.id, update_data, user)

    async def delete_mark(self, mark_id: int, user: User):
        mark = await self._check_mark_ownership(mark_id, user)
        result = await self.mark_repo.delete_mark(mark.id)
        return result

    async def _check_mark_ownership(self, mark_id: int, user: User) -> Mark:
        mark = await self.mark_repo.get_mark_by_id(mark_id)
        if not mark:
            raise RecordNotFoundError()
        if mark.owner_id != user.id:
            raise UserPermissionError(status_code=403)
        return mark

    async def _check_category_exist(self, category_id: int) -> None:
        category_exist = await self.category_repo.exist(category_id)
        if not category_exist:
            raise RecordNotFoundError()

    @staticmethod
    def _check_timeout(mark: Mark, duration: int = 1):
        passed_time = datetime.now() - mark.created_at
        if passed_time > timedelta(hours=duration):
            raise TimeOutError()
