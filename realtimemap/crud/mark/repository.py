from datetime import timedelta
from typing import List, TYPE_CHECKING, Union

from fastapi import HTTPException
from geoalchemy2.functions import (
    ST_SetSRID,
    ST_MakePoint,
    ST_DWithin,
    ST_Transform,
    ST_AsGeoJSON,
    ST_Distance,
)
from sqlalchemy import select

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

if TYPE_CHECKING:
    from models import User
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkRepository(BaseRepository[Mark, CreateMark, ReadMark, UpdateMark]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(Mark, session, "id")
        self.upload_dir = "upload_marks"

    async def get_marks(self, params: MarkRequestParams) -> List[Mark]:
        current_point = ST_SetSRID(
            ST_MakePoint(params.longitude, params.latitude), params.srid
        )

        # Вычисляем границы временного окна (используем Python timedelta для параметров)
        min_start = params.date - timedelta(hours=params.duration)
        max_end = params.date + timedelta(hours=params.duration)

        conditions = [
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

        query = select(self.model, ST_AsGeoJSON(self.model.geom).label("geom")).where(
            *conditions
        )

        result = await self.session.execute(query)

        return result.scalars().all()

    @staticmethod
    def _preparation_data(
        mark: Union[CreateMarkRequest, UpdateMarkRequest], user: "User"
    ) -> CreateMark:
        geom = f"SRID=4326;POINT({mark.longitude} {mark.latitude})"
        mark_data = mark.model_dump(exclude={"longitude", "latitude"})
        formated_data = CreateMark(**mark_data, geom=geom, owner_id=user.id)
        return formated_data

    async def create_mark(self, mark: CreateMarkRequest, user: "User") -> Mark:
        data = self._preparation_data(mark, user)
        result: Mark = await super().create(data)

        return result

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        stmt = select(self.model).where(self.model.id == mark_id)
        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=404, detail="mark not found")

        return result

    async def delete_mark(self, mark_id: int, user: "User") -> Mark:
        mark = await self.get_mark_by_id(mark_id)
        if not mark.owner == user:
            raise HTTPException(status_code=403)
        await super().delete(mark_id)
        return mark

    async def check_distance(
        self, current_location: MarkRequestParams, mark: Mark, radius: int = 500
    ) -> bool:
        user_point = ST_SetSRID(
            ST_MakePoint(current_location.longitude, current_location.latitude), 4326
        )

        print(type(mark.geom))
        stmt = select(
            ST_Distance(ST_Transform(mark.geom, 3857), ST_Transform(user_point, 3857))
            <= radius
        )

        result = await self.session.execute(stmt)
        return result.scalar()

    async def update_mark(
        self, mark_id: int, update_data: UpdateMarkRequest, user: "User"
    ) -> Mark:
        geom = f"SRID=4326;POINT({update_data.longitude} {update_data.latitude})"
        mark_data = update_data.model_dump(
            exclude={"longitude", "latitude"}, exclude_unset=True
        )
        formated_data = UpdateMark(**mark_data, geom=geom, owner_id=user.id)
        return await self.update(mark_id, formated_data)
