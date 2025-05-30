from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """
    Base class for all services.
    """

    def __init__(self, session: "AsyncSession"):
        self.session = session
