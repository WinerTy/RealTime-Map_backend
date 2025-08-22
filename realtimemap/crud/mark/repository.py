from datetime import timedelta
from typing import List, TYPE_CHECKING, Union, Type

from fastapi import HTTPException
from geoalchemy2.functions import (
    ST_SetSRID,
    ST_MakePoint,
    ST_DWithin,
    ST_Transform,
    ST_AsGeoJSON,
    ST_DistanceSphere,
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
from utils.geom.geom_sector import get_geohash, get_neighbors

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from models import User


class MarkRepository(BaseRepository[Mark, CreateMark, ReadMark, UpdateMark]):
    def __init__(self, session: AsyncSession):
        super().__init__(Mark, session, "id")
        self.upload_dir = "upload_marks"

    async def get_marks(self, params: MarkRequestParams) -> List[Mark]:
        current_point = ST_SetSRID(
            ST_MakePoint(params.longitude, params.latitude), params.srid
        )

        # Работа с geohash для фильтрации по зонам
        geohash = get_geohash(params.latitude, params.longitude)
        neighbors = get_neighbors(geohash)
        neighbors.append(geohash)

        # Вычисляем границы временного окна (используем Python timedelta для параметров)
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

    @staticmethod
    def _preparation_data(
        mark: Union[CreateMarkRequest, UpdateMarkRequest],
        user: User,
        response_class: Type[BaseModel],
    ) -> Type[BaseModel]:
        geom = None
        if mark.longitude and mark.latitude:
            geom = f"SRID=4326;POINT({mark.longitude} {mark.latitude})"
        mark_data = mark.model_dump(exclude={"longitude", "latitude"})
        formated_data = response_class(
            **mark_data,
            geom=geom,
            owner_id=user.id,
            geohash=get_geohash(mark.latitude, mark.longitude),
        )
        return formated_data

    async def create_mark(self, mark: CreateMarkRequest, user: "User") -> Mark:
        data = self._preparation_data(mark, user, CreateMark)
        result: Mark = await super().create(data)
        await self.session.refresh(result, ["category"])
        return result

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        stmt = select(self.model).where(self.model.id == mark_id)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=404, detail="mark not found")

        return result

    async def delete_mark(self, mark_id: int, user: User) -> Mark:
        mark = await self.get_mark_by_id(mark_id)
        if not mark.owner == user:
            raise HTTPException(status_code=403)
        await super().delete(mark_id)
        return mark

    async def check_distance(
        self, current_location: MarkRequestParams, mark: Mark, radius: int = 500
    ) -> bool:
        # Проверка вложена ли метка в зону
        geohash = get_geohash(current_location.latitude, current_location.longitude)

        if mark.geohash not in [geohash] + get_neighbors(geohash):
            return False

        # Проверка вложена ли метка в радиус пользователя
        user_point = ST_SetSRID(
            ST_MakePoint(current_location.longitude, current_location.latitude), 4326
        )

        stmt = select(ST_DistanceSphere(mark.geom, user_point, radius))

        result = await self.session.execute(stmt)
        return result.scalar()

    async def update_mark(
        self, mark_id: int, update_data: UpdateMarkRequest, user: User
    ) -> Mark:
        formated_data = self._preparation_data(update_data, user, UpdateMark)
        return await self.update(mark_id, formated_data)
