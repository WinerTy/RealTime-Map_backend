from typing import TYPE_CHECKING

from fastapi import HTTPException
from fastapi_babel import _

from models import User
from models.mark.schemas import ReadMark, CreateMarkRequest
from services.base import BaseService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from crud.mark import MarkRepository
    from crud.category import CategoryRepository


class MarkService(BaseService):
    def __init__(
        self,
        session: "AsyncSession",
        mark_repo: "MarkRepository",
        category_repo: "CategoryRepository",
    ):
        super().__init__(session)
        self.mark_repo = mark_repo
        self.category_repo = category_repo

    async def service_create_mark(
        self, mark_data: CreateMarkRequest, user: User
    ) -> ReadMark:
        category_exist = await self.category_repo.exist(mark_data.category_id)
        if not category_exist:
            raise HTTPException(
                status_code=422,
                detail=_(f"Category with id {mark_data.category_id} not found."),
            )
        mark = await self.mark_repo.create_mark(mark_data, user)
        return mark
