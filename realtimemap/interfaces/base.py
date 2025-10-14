from typing import Protocol, Dict, Optional, Union, List, Any

from sqlalchemy.orm import joinedload

from my_type import Model, CreateSchema, UpdateSchema


class IBaseRepository(Protocol[Model, CreateSchema, UpdateSchema]):
    async def get_by_id(
        self,
        item_id: Any,
        join_related: Optional[Union[List[str], Dict[str, Any]]] = None,
        load_strategy: Any = joinedload,
    ) -> Optional[Model]: ...

    async def get_by_name(self, name: str) -> Optional[Model]: ...

    async def create(self, data: CreateSchema, *kwargs) -> Model: ...

    async def update(self, item_id: Any, data: UpdateSchema) -> Model: ...

    async def delete(self, record_id: Any) -> Model:
        """Delete record by id
        :param record_id: record id
        :return: Model instance from Generic
        """
        ...

    async def exist(self, record_id: int) -> bool:
        """
        Check if record id exists.
        :param record_id: record id
        """
        ...
