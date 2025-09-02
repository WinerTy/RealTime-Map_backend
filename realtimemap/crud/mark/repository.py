from __future__ import annotations

from datetime import timedelta
from typing import List, TYPE_CHECKING, Union, Type, Optional

from geoalchemy2.functions import (
    ST_DWithin,
    ST_Transform,
    ST_AsGeoJSON,
)
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from crud import BaseRepository
from models import Mark
from models.mark.schemas import (
    CreateMark,
    ReadMark,
    UpdateMark,
    CreateMarkRequest,
    MarkRequestParams,
    UpdateMarkRequest,
)
from services.geo.service import GeoService

if TYPE_CHECKING:
    from models import User


class MarkRepository(BaseRepository[Mark, CreateMark, ReadMark, UpdateMark]):
    """
    Repository for the Mark model.
    """

    def __init__(
        self, session: "AsyncSession", geo_service: Optional[GeoService] = None
    ):
        super().__init__(Mark, session, "id")
        self.upload_dir = "upload_marks"
        self.geo_service = geo_service if geo_service is not None else GeoService()

    async def get_marks(self, params: MarkRequestParams) -> List[Mark]:
        current_point = self.geo_service.create_point(params, params.srid)

        # Preparation geohash sectors
        neighbors = self.geo_service.get_neighbors(
            self.geo_service.get_geohash(params), True
        )

        # Time
        min_start = params.date - timedelta(hours=params.duration)
        max_end = params.date + timedelta(hours=params.duration)
        # Условия фильтрации
        conditions = [
            self.model.geohash.in_(neighbors),
            ST_DWithin(
                ST_Transform(self.model.geom, 3857),
                ST_Transform(current_point, 3857),
                params.radius,
            ),
            self.model.start_at <= max_end,
            self.model.start_at + timedelta(hours=params.duration) >= min_start,
        ]
        if not params.show_ended:
            conditions.append(self.model.is_ended == params.show_ended)

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
            geohash=self.geo_service.get_geohash(mark),
        )
        return formated_data

    async def create_mark(self, mark: CreateMarkRequest, user: "User") -> Mark:
        """
        Method for creating a new mark
        Args:
            mark (CreateMarkRequest): CreateMark request (All needed data)
            user (User): User. Who created the new mark
        Returns:
            Mark: Created mark
        Raises: Need for next version
        """
        data = self.preparation_data(mark, user, CreateMark)
        result: Mark = await super().create(data)
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
        stmt = select(self.model).where(self.model.id == mark_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

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

    async def check_distance(
        self, current_location: MarkRequestParams, mark: Mark, radius: int = 500
    ) -> bool:
        """
        Method for checking if the given location is within the given radius.

        Args:
            current_location (MarkRequestParams): Current location
            mark (Mark): Mark to check
            radius (int): Radius to check. Need for SQL expression

        Returns:
            bool: True or False
        """
        # Проверка вложена ли метка в зону
        geohash = self.geo_service.get_geohash(current_location)
        neighbors = self.geo_service.get_neighbors(geohash, need_include=True)

        if mark.geohash not in neighbors:
            return False

        # Проверка вложена ли метка в радиус пользователя
        user_point = self.geo_service.create_point(current_location)
        exp = self.geo_service.distance_sphere(user_point, mark.geom, radius)

        stmt = select(exp)

        result = await self.session.execute(stmt)
        return result.scalar()

    async def update_mark(
        self, mark_id: int, update_data: UpdateMarkRequest, user: "User"
    ) -> Mark:
        formated_data = self.preparation_data(update_data, user, UpdateMark)
        return await self.update(mark_id, formated_data)
