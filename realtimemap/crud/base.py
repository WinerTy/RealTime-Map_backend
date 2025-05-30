import logging
from typing import Generic, Type, Any

from fastapi import HTTPException
from fastapi_babel import _  # noqa
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import exists as sql_exists
from starlette.responses import Response

from my_type import Model, CreateSchema, ReadSchema, UpdateSchema

logger = logging.getLogger(__name__)


class BaseRepository(Generic[Model, CreateSchema, ReadSchema, UpdateSchema]):
    def __init__(
        self,
        model: Type[Model],
        session: AsyncSession,
        id_field: str = "id",
    ):
        self.model: Type[Model] = model
        self.session: AsyncSession = session
        self.id_field: str = id_field

    async def get_by_id(
        self,
        item_id: Any,
    ) -> Model:
        """
        Получает объект из базы данных по его идентификатору.

        Args:
            item_id: Идентификатор объекта (int, str или UUID в зависимости от модели).

        Returns:
            Model: Найденный объект модели. Если объект не найден и raise_ex=False, возвращает None.

        Raises:
            HTTPException: Исключение с кодом 404, если объект не найден и raise_ex=True.
        """
        stmt = select(self.model).where(getattr(self.model, self.id_field) == item_id)
        result = await self.session.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail="Record not found")
        return instance

    async def create(self, data: CreateSchema, *kwargs) -> Model:
        try:
            logger.info(f"Create record {data} in Repository: {self.model.__name__}")
            data = data.model_dump()
            data.update(kwargs)

            db_item = self.model(**data)
            self.session.add(db_item)
            await self.session.commit()
            await self.session.refresh(db_item)
            return db_item
        except IntegrityError:
            logger.info(
                f"Record {data} already exists in Repository: {self.model.__name__}"
            )
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=_("Record already exists"))
        except Exception as e:
            logger.error(
                f"Create record {data} in Repository: {self.model.__name__}", e
            )
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error in Repository Class, please check create method. {str(e)}",
            )

    async def delete(self, record_id: Any) -> None:
        try:
            record = await self.get_by_id(record_id)
            stmt = delete(self.model).where(
                getattr(self.model, self.id_field) == record.id
            )
            logger.info(
                f"Delete record {record_id} in Repository: {self.model.__name__}. Query: {stmt}"
            )
            await self.session.execute(stmt)
            await self.session.commit()
            return Response(status_code=204)
        except Exception as e:
            logger.error(
                f"Delete record {record_id} by id in Repository: {self.model.__name__}. ",
                e,
            )
            await self.session.rollback()

    async def exist(self, record_id: int) -> bool:
        stmt = select(sql_exists().where(self.model.id == record_id))
        result = await self.session.execute(stmt)
        return result.scalar_one()
