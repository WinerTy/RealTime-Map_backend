from typing import Generic, Type, Any

from fastapi import HTTPException
from fastapi_babel import _  # noqa
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from my_type import Model, CreateSchema, ReadSchema, UpdateSchema


class BaseRepository(Generic[Model, CreateSchema, ReadSchema, UpdateSchema]):
    def __init__(self, model: Type[Model], session: AsyncSession, id_field: str = "id"):
        self.model: Type[Model] = model
        self.session: AsyncSession = session
        self.id_field: str = id_field

    async def get_by_id(self, record_id: Any):
        """Метод для получения записи по ID"""
        try:
            query = select(self.model).where(self.id_field == record_id)
            instance = await self.session.execute(query)
            instance = instance.scalar_one_or_none()
            if not instance:
                raise HTTPException(
                    status_code=404, detail=_(f"Record with id: {record_id} not found")
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error in Repository Class, please check get_by_id. {str(e)}",
            )

    async def create(self, data: CreateSchema, *kwargs) -> Model:
        try:
            data = data.model_dump()
            data.update(kwargs)

            db_item = self.model(**data)
            self.session.add(db_item)
            await self.session.commit()
            await self.session.refresh(db_item)
            return db_item
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=_("Record already exists"))
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error in Repository Class, please check create method. {str(e)}",
            )
