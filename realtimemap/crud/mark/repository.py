import json
from typing import Optional, List, TYPE_CHECKING

from geoalchemy2.functions import (
    ST_SetSRID,
    ST_MakePoint,
    ST_DWithin,
    ST_Transform,
    ST_AsGeoJSON,
)
from sqlalchemy import select

from crud import BaseRepository
from models import Mark, TypeMark, User
from schemas.mark import CreateMark, ReadMark, UpdateMark, CreateMarkRequest
from utils import upload_file

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class MarkRepository(BaseRepository[Mark, CreateMark, ReadMark, UpdateMark]):
    def __init__(self, session: "AsyncSession"):
        super().__init__(Mark, session, "id")
        self.upload_dir = "upload_marks"

    async def get_marks(
        self,
        longitude: float,
        latitude: float,
        radius: int = 500,
        type_mark: Optional[TypeMark] = None,
        srid: int = 4326,
    ) -> List[ReadMark]:
        current_point = ST_SetSRID(ST_MakePoint(longitude, latitude), srid)
        conditions = [
            ST_DWithin(
                ST_Transform(self.model.geom, 3857),
                ST_Transform(current_point, 3857),
                radius,
            )
        ]

        if type_mark:
            conditions.append(self.model.type_mark == type_mark)

        query = select(self.model, ST_AsGeoJSON(self.model.geom).label("geom")).where(
            *conditions
        )

        result = await self.session.execute(query)
        return [
            ReadMark(
                id=mark.id,
                mark_name=mark.mark_name,
                type_mark=mark.type_mark,
                geom=json.loads(coords),
            )
            for mark, coords in result
        ]

    async def create_mark(self, mark: CreateMarkRequest, user: "User") -> Mark:
        geom = f"SRID=4326;POINT({mark.longitude} {mark.latitude})"
        mark_data = mark.model_dump(exclude={"longitude", "latitude", "photo"})
        if mark.photo:
            file_path = await upload_file(mark.photo, self.upload_dir)
            mark_data["photo"] = file_path
        formated_data = CreateMark(**mark_data, geom=geom, owner_id=user.id)
        result: Mark = await super().create(formated_data)

        return result

    async def get_all_marks(self):
        stmt = select(self.model, ST_AsGeoJSON(self.model.geom).label("geom"))

        result = await self.session.execute(stmt)
        # marks_list = []
        deb_res = [
            {
                "id": mark.id,
                "mark_name": mark.mark_name,
                "type_mark": mark.type_mark,
                "geom": json.loads(coords),
            }
            for mark, coords in result
        ]

        return deb_res

    async def get_mark_by_id(self, mark_id: int) -> Mark:
        mark = await self.get_by_id(mark_id)
        return mark
