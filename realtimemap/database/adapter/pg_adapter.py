import logging
from typing import (
    Type,
    TYPE_CHECKING,
)

from my_type import Model, CreateSchema, UpdateSchema
from .sqlachemy_adapter import SQLAlchemyAdapter

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class PgAdapter(SQLAlchemyAdapter[Model, CreateSchema, UpdateSchema]):
    """
    PostgreSQL adapter implementing BaseAdapter interface.
    Provides concrete implementations for all database operations using SQLAlchemy.
    """

    def __init__(
        self,
        session: "AsyncSession",
        model: Type[Model],
    ):
        """
        Initialize PostgreSQL adapter.

        Args:
            model: SQLAlchemy model class
            session: Async database session
        """
        super().__init__(session, model)
