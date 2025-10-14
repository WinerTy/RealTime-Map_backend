from typing import TypeVar, Protocol

from pydantic import BaseModel

from models import Base


class ModelWithId(Protocol):
    id: int


# TODO CHANGE TO BASESQL CLASS
Model = TypeVar("Model", bound=Base)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
