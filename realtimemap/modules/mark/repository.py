from datetime import timedelta
from typing import TYPE_CHECKING, Optional, List

from geoalchemy2.functions import ST_DWithin, ST_Transform, ST_AsGeoJSON
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from core.common.repository import MarkRepository
from database.adapter import PgAdapter
from modules.geo_service import GeoService
from .filters import MarkFilter
from .model import Mark
from .schemas import CreateMark, UpdateMark

if TYPE_CHECKING:
    pass


class PgMarkRepository(MarkRepository):
    """
    Repository for the Mark model for PostgreSQL.
    """

    def __init__(
        self,
        adapter: PgAdapter[Mark, CreateMark, UpdateMark],
        geo_service: Optional[GeoService] = None,
    ):
        super().__init__(adapter)
        self.geo_service = geo_service if geo_service is not None else GeoService()
        self.adapter = adapter

    async def get_marks(self, filters: "MarkFilter") -> List[Mark]:
        # Условия фильтрации
        conditions = [
            Mark.geohash.in_(filters.geohash_neighbors),
            ST_DWithin(
                ST_Transform(Mark.geom, 3857),
                ST_Transform(filters.current_point, 3857),
                filters.radius,
            ),
            Mark.start_at <= filters.max_end,
            Mark.start_at + timedelta(hours=filters.duration) >= filters.min_start,
        ]
        if not filters.show_ended:
            conditions.append(Mark.is_ended == filters.show_ended)

        query = (
            select(Mark, ST_AsGeoJSON(Mark.geom).label("geom"))
            .where(*conditions)
            .options(joinedload(Mark.category))
        )

        return await self.adapter.execute_query(query)

    async def create_mark(self, mark: CreateMark) -> Mark:
        """
        Method for creating a new mark
        Args:
            mark (CreateMark): valid data for the new mark
        Returns:
            Mark: Created mark
        Raises: Need for next version
        """
        result = await self.adapter.create(mark, join_related=["category"])
        return result

    async def delete_mark(self, mark_id: int) -> Mark:
        """
        Method for deleting a mark by its id
        Args:
            mark_id (int): The id of the mark
        Returns:
            Mark (Mark): The mark
        """
        mark = await self.get_by_id(mark_id)
        await super().delete(mark_id)
        return mark

    async def check_distance(self, filters: "MarkFilter", mark: Mark) -> bool:
        # Проверка вложена ли метка в радиус пользователя
        exp = self.geo_service.distance_sphere(
            filters.current_point, mark.geom, filters.radius
        )

        stmt = select(exp)

        distance = await self.adapter.execute_scalar(stmt)
        return distance <= filters.radius

    async def update_mark(self, mark_id: int, update_data: UpdateMark) -> Mark:
        return await self.adapter.update(mark_id, update_data)
