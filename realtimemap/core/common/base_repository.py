import logging
from abc import ABC, abstractmethod
from typing import (
    Generic,
    Type,
    Any,
    Optional,
    List,
    Union,
    Dict,
    TYPE_CHECKING,
)

from sqlalchemy import select, delete, Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import exists as sql_exists

from errors.http2 import IntegrityError as RealTimeMapIntegrityError, ServerError
from my_type import Model, CreateSchema, UpdateSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class IBaseRepository(ABC):
    @abstractmethod
    async def create(self, data: CreateSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: UpdateSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        item_id: Any,
        join_related: Optional[Union[List[str], Dict[str, Any]]] = None,
        load_strategy: Any = joinedload,
    ) -> Optional[Model]:
        raise NotImplementedError


class BaseRepository(Generic[Model, CreateSchema, UpdateSchema]):
    def __init__(
        self,
        model: Type[Model],
        session: "AsyncSession",
        id_field: str = "id",
    ):
        self.model: Type[Model] = model
        self.session: "AsyncSession" = session
        self.id_field: str = id_field

    async def get_by_id(
        self,
        item_id: Any,
        join_related: Optional[Union[List[str], Dict[str, Any]]] = None,
        load_strategy: Any = joinedload,
    ) -> Optional[Model]:
        stmt: Select[Any] = select(self.model).where(
            getattr(self.model, self.id_field) == item_id
        )
        if join_related:
            if isinstance(join_related, list):
                for relation in join_related:
                    # Получаем реальный атрибут модели по строковому имени
                    relation_attr = getattr(self.model, relation)
                    stmt = stmt.options(load_strategy(relation_attr))
            elif isinstance(join_related, dict):
                for relation, strategy in join_related.items():
                    relation_attr = getattr(self.model, relation)
                    stmt = stmt.options(strategy(relation_attr))

        result = await self.session.execute(stmt)
        instance = result.scalars().first()
        return instance

    async def create(self, data: CreateSchema, *kwargs: Any) -> Model:
        try:
            logger.info(f"Create record {data} in Repository: {self.model.__name__}")
            dict_data: Dict[str, Any] = data.model_dump()
            dict_data.update(kwargs)

            db_item = self.model(**dict_data)
            self.session.add(db_item)
            await self.session.flush()
            await self.session.refresh(db_item)
            return db_item
        except IntegrityError:
            logger.info(
                f"Record {data} already exists in Repository: {self.model.__name__}"
            )
            await self.session.rollback()
            raise RealTimeMapIntegrityError()
        except Exception as e:
            logger.error(
                f"Create record {data} in Repository: {self.model.__name__}", exc_info=e
            )
            await self.session.rollback()
            raise ServerError()

    async def update(self, item_id: Any, data: UpdateSchema) -> Optional[Model]:
        try:
            instance = await self.get_by_id(item_id)

            if instance is None:
                return None

            update_data = data.model_dump(exclude_unset=True, exclude_none=True)

            # Update attributes
            for k, v in update_data.items():
                setattr(instance, k, v)

            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)

            return instance
        except Exception:
            logger.error(f"Update record in {self.model.__name__}, data: {data}")
            await self.session.rollback()
            raise ServerError()

    async def delete(self, record_id: Any) -> Optional[Model]:
        try:
            record = await self.get_by_id(record_id)

            if record is None:
                return None

            stmt = delete(self.model).where(
                getattr(self.model, self.id_field) == record.id
            )

            logger.info(
                f"Delete record {record_id} in Repository: {self.model.__name__}. Query: {stmt}"
            )

            await self.session.execute(stmt)
            await self.session.flush()

            return record
        except Exception as e:
            logger.error(
                f"Delete record {record_id} by id in Repository: {self.model.__name__}. ",
                e,
            )
            await self.session.rollback()
            return None

    async def exist(self, record_id: int) -> bool:
        stmt = select(sql_exists().where(self.model.id == record_id))
        result = await self.session.execute(stmt)
        return result.scalar_one()
