from typing import Any, Dict, TYPE_CHECKING, Optional

from sqlalchemy import MetaData, select, func, and_
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import conf
from modules.mixins import IntIdMixin
from utils import camel_case_to_snake_case

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from starlette.requests import Request


class BaseSqlModel(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=conf.db.naming_convention)

    @classmethod
    def _validate_filter_fields(cls, filters: Dict[str, Any]):
        for key, value in filters.items():
            if not hasattr(cls, key):
                raise AttributeError(f"Class {cls.__name__} has no attribute {key}")

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa
        return camel_case_to_snake_case(cls.__name__) + "s"

    @classmethod
    async def count(
        cls,
        session: "AsyncSession",
        filters: Optional[Dict[str, Any]] = None,
    ):
        if filters:
            cls._validate_filter_fields(filters)

        stmt = select(func.count()).select_from(cls)
        if filters:
            filter_conditions = []
            for field_name, value in filters.items():
                column_attr = getattr(cls, field_name)
                filter_conditions.append(column_attr == value)

            if filter_conditions:
                stmt = stmt.where(and_(*filter_conditions))
        result = await session.execute(stmt)
        count_value = result.scalar_one()
        return count_value

    async def __admin_repr__(self, _: "Request") -> str:
        return self.__class__.__name__

    async def __admin_select2_repr__(self, _: "Request") -> str:
        return self.__class__.__name__


class Base(BaseSqlModel, IntIdMixin):
    pass
