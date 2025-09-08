from typing import TypeVar, Protocol

from pydantic import BaseModel

from models import BaseSqlModel


class ModelWithId(Protocol):
    id: int


# TODO CHANGE TO BASESQL CLASS
Model = TypeVar("Model", bound=BaseSqlModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
