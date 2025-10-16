from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from errors import RecordNotFoundError, UserPermissionError, TimeOutError
from models import User, Mark
from models.mark.schemas import (
    CreateMarkRequest,
    MarkRequestParams,
    UpdateMarkRequest,
    MarkFilter,
    CreateMark,
    CreateTestMarkRequest,
)
from services.base import BaseService
from services.geo.service import GeoService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from interfaces import IMarkRepository, ICategoryRepository, IMarkCommentRepository


class MarkService(BaseService):
    def __init__(
        self,
        session: "AsyncSession",
        mark_repo: "IMarkRepository",
        category_repo: "ICategoryRepository",
        mark_comment_repo: "IMarkCommentRepository",
        geo_service: "GeoService",
    ):
        super().__init__(session)
        self.mark_repo = mark_repo
        self.category_repo = category_repo
        self.mark_comment_repo = mark_comment_repo
        self.geo_service = geo_service

    def _validate__create_data(
        self, data: CreateMarkRequest, user: "User"
    ) -> CreateMark:
        geom = None
        if data.longitude and data.latitude:
            geom = self.geo_service.create_geometry_point(data)
        return CreateMark(
            **data.model_dump(exclude={"latitude", "longitude"}),
            owner_id=user.id,
            geom=geom,
            geohash=(
                self.geo_service.get_geohash(data)
                if data.longitude and data.latitude
                else None
            ),
        )

    async def create_mark(self, mark_data: CreateMarkRequest, user: User) -> Mark:
        category_exist = await self.category_repo.exist(mark_data.category_id)
        if not category_exist:
            raise RecordNotFoundError()
        create_data = self._validate__create_data(mark_data, user)
        mark = await self.mark_repo.create_mark(create_data)
        return mark

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        result = await self.mark_repo.get_by_id(
            mark_id, join_related=["owner", "category"]
        )
        if not result:
            raise RecordNotFoundError()
        return result

    async def get_marks(self, params: MarkRequestParams):
        filters = MarkFilter.from_request(params, self.geo_service)
        result = await self.mark_repo.get_marks(filters)
        return result

    async def delete_mark(self, mark_id: int, user: User):
        mark = await self.get_mark_by_id(mark_id)
        await self._check_mark_ownership(mark, user)
        result = await self.mark_repo.delete_mark(mark.id)
        return result

    async def update_mark(
        self, user: User, update_data: UpdateMarkRequest, mark_id: int
    ) -> Mark:
        mark = await self.mark_repo.get_mark_by_id(mark_id)
        await self._before_update_mark(mark, user, update_data)
        return await self.mark_repo.update_mark(mark.id, update_data, user)

    async def _before_update_mark(
        self, mark: Mark, user: User, update_data: UpdateMarkRequest
    ) -> Mark:
        """
        The method is called before updating
        1. Checks the existence of the selected category
        2. Checking the existence of a post and the author of the post
        3. Checking for editing timeout
        If additional checks are needed, add below
        """
        await self._check_category_exist(update_data)
        await self._check_mark_ownership(mark, user)
        self._check_timeout(mark)
        return mark

    @staticmethod
    async def _check_mark_ownership(mark: Mark, user: User) -> None:
        if not mark:
            raise RecordNotFoundError()
        if mark.owner_id != user.id:
            raise UserPermissionError(status_code=403)

    async def _check_category_exist(self, update_data: UpdateMarkRequest) -> None:
        if not update_data.category_id:
            return

        category_exist = await self.category_repo.exist(update_data.category_id)
        if not category_exist:
            raise RecordNotFoundError()

    @staticmethod
    def _check_timeout(mark: Mark, duration: int = 1):
        passed_time = datetime.now() - mark.created_at
        if passed_time > timedelta(hours=duration):
            raise TimeOutError()

    async def create_test_mark(self, params: CreateTestMarkRequest):
        res = await self.mark_repo.get_ids_for_test()
        print(res)
