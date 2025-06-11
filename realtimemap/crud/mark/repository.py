import json
from datetime import timedelta
from typing import List, TYPE_CHECKING

from fastapi import HTTPException
from geoalchemy2.functions import (
    ST_SetSRID,
    ST_MakePoint,
    ST_DWithin,
    ST_Transform,
    ST_AsGeoJSON,
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
)

if TYPE_CHECKING:
    from models import User
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkRepository(BaseRepository[Mark, CreateMark, ReadMark, UpdateMark]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(Mark, session, "id")
        self.upload_dir = "upload_marks"

    async def get_marks(self, params: MarkRequestParams) -> List[ReadMark]:
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
            # Метка должна начаться не позже max_end
            self.model.start_at <= max_end,
            # И закончиться не раньше min_start (используем SQL-функции для вычисления)
            self.model.start_at + timedelta(hours=params.duration) >= min_start,
        ]
        if not params.show_ended:
            conditions.append(self.model.is_ended == params.show_ended)

        query = select(self.model, ST_AsGeoJSON(self.model.geom).label("geom")).where(
            *conditions
        )

        result = await self.session.execute(query)
        result_list = []

        for mark, coords in result:
            mark_data = mark.__dict__
            mark_data.pop("geom")
            mark_data["end_at"] = mark.end_at
            result_list.append(ReadMark(**mark_data, geom=json.loads(coords)))

        return result_list

    async def create_mark(self, mark: CreateMarkRequest, user: "User") -> Mark:
        geom = f"SRID=4326;POINT({mark.longitude} {mark.latitude})"
        mark_data = mark.model_dump(exclude={"longitude", "latitude"})
        # if mark.photo:
        #     file_path = await upload_file(mark.photo, self.upload_dir)
        #     mark_data["photo"] = file_path
        formated_data = CreateMark(**mark_data, geom=geom, owner_id=user.id)
        result: Mark = await super().create(formated_data)

        return result

    async def get_mark_by_id(self, mark_id: int) -> ReadMark:
        stmt = select(self.model, ST_AsGeoJSON(self.model.geom).label("geom")).where(
            self.model.id == mark_id
        )
        result = await self.session.execute(stmt)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="mark not found")

        print(result)
        mark = result[0]
        coords = result[1]
        mark_data = mark.__dict__
        mark_data["end_at"] = mark.end_at
        mark_data.pop("geom")
        return ReadMark(**mark_data, geom=json.loads(coords))

    async def delete_mark(self, mark_id: int, user: "User") -> None:
        mark = await self.get_mark_by_id(mark_id)
        if not mark.owner == user:
            raise HTTPException(status_code=403)
        await super().delete(mark_id)
