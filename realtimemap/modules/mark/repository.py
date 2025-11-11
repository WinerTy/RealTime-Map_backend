from datetime import timedelta
from typing import TYPE_CHECKING, Optional, Sequence

from geoalchemy2.functions import ST_DWithin, ST_Transform, ST_AsGeoJSON
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.common import BaseRepository
from modules.geo_service import GeoService
from .filters import MarkFilter
from .model import Mark
from .schemas import CreateMark, UpdateMark

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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

    async def get_marks(self, filters: MarkFilter) -> Sequence[Mark]:
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
        # Проверка вложена ли метка в радиус пользователя
        exp = self.geo_service.distance_sphere(
            filters.current_point, mark.geom, filters.radius
        )

        stmt = select(exp)

        result = await self.session.execute(stmt)
        distance = result.scalar()
        return distance <= filters.radius

    async def update_mark(self, mark_id: int, update_data: UpdateMark) -> Mark:
        return await self.update(mark_id, update_data)
