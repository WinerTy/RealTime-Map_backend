from __future__ import annotations

import logging
from datetime import timedelta
from typing import List, TYPE_CHECKING, Union, Type, Optional, Tuple, Sequence

from geoalchemy2.functions import (
    ST_DWithin,
    ST_Transform,
    ST_AsGeoJSON,
)
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from crud import BaseRepository
from models import Mark, Category
from models import User
from models.mark.schemas import (
    CreateMark,
    UpdateMark,
    CreateMarkRequest,
    UpdateMarkRequest,
    MarkFilter,
)
from services.geo.service import GeoService

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class MarkRepository(BaseRepository[Mark, CreateMark, UpdateMark]):
    """
    Repository for the Mark model.
    """

    def __init__(
        self, session: "AsyncSession", geo_service: Optional[GeoService] = None
    ):
        super().__init__(Mark, session, "id")
        self.upload_dir = "upload_marks"
        self.geo_service = geo_service if geo_service is not None else GeoService()

    async def get_marks(self, filters: MarkFilter) -> List[Mark]:
        # Условия фильтрации
        conditions = [
            self.model.geohash.in_(filters.geohash_neighbors),
            ST_DWithin(
                ST_Transform(self.model.geom, 3857),
                ST_Transform(filters.current_point, 3857),
                filters.radius,
            ),
            self.model.start_at <= filters.max_end,
            self.model.start_at + timedelta(hours=filters.duration)
            >= filters.min_start,
        ]
        if not filters.show_ended:
            conditions.append(self.model.is_ended == filters.show_ended)

        query = (
            select(self.model, ST_AsGeoJSON(self.model.geom).label("geom"))
            .where(*conditions)
            .options(joinedload(self.model.category))
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    def preparation_data(
        self,
        mark: Union[CreateMarkRequest, UpdateMarkRequest],
        user: "User",
        response_class: Type[BaseModel],
    ) -> Type[BaseModel]:
        """
        Method for preparation raw data.
        Args:
            mark (CreateMarkRequest or UpdateMarkRequest): raw data for creating or updating a mark
            user (User): User who make action
            response_class (Type[BaseModel]): Class for response preparation data
        Returns:
            Type[BaseModel]: Prepared data
        """
        geom = None
        if mark.longitude and mark.latitude:
            geom = self.geo_service.create_geometry_point(mark)
        mark_data = mark.model_dump(exclude={"longitude", "latitude"})
        formated_data = response_class(
            **mark_data,
            geom=geom,
            owner_id=user.id,
            geohash=(
                self.geo_service.get_geohash(mark)
                if mark.longitude and mark.latitude
                else None
            ),
        )
        return formated_data

    async def create_mark(self, mark: CreateMark) -> Mark:
        """
        Method for creating a new mark
        Args:
            mark (CreateMarkRequest): CreateMark request (All needed data)
        Returns:
            Mark: Created mark
        Raises: Need for next version
        """
        result: Mark = await super().create(mark)
        await self.session.refresh(result, ["category"])
        return result

    async def get_mark_by_id(self, mark_id: int) -> Optional[Mark]:
        """
        Method for getting a mark by its id
        Args:
            mark_id (int): The id of the mark
        Returns:
            Mark (Mark): The mark
        Raises:
            HTTPException: 404 if the mark is not found
        """
        result = await self.get_by_id(mark_id, join_related=["category"])
        return result

    async def delete_mark(self, mark_id: int) -> Mark:
        """
        Method for deleting a mark by its id
        Args:
            mark_id (int): The id of the mark
        Returns:
            Mark (Mark): The mark
        """
        mark = await self.get_mark_by_id(mark_id)
        await super().delete(mark_id)
        return mark

    async def check_distance(self, filters: MarkFilter, mark: Mark) -> bool:
        if mark.geohash not in filters.geohash_neighbors:
            return False

        # Проверка вложена ли метка в радиус пользователя
        exp = self.geo_service.distance_sphere(
            filters.current_point, mark.geom, filters.radius
        )

        stmt = select(exp)

        result = await self.session.execute(stmt)
        distance = result.scalar()
        return distance <= filters.radius

    async def update_mark(
        self, mark_id: int, update_data: UpdateMarkRequest, user: "User"
    ) -> Mark:
        formated_data = self.preparation_data(update_data, user, UpdateMark)
        return await self.update(mark_id, formated_data)

    async def get_ids_for_test(self) -> Tuple[Sequence[int], Sequence[int]]:
        stmt = select(User.id).limit(10)
        users_ids = await self.session.execute(stmt)
        users_ids = users_ids.scalars().all()
        stmt = select(Category.id)
        category_ids = await self.session.execute(stmt)
        category_ids = category_ids.scalars().all()
        return users_ids, category_ids
