from typing import TypeVar

from pydantic import BaseModel

from modules import BaseSqlModel

Model = TypeVar("Model", bound=BaseSqlModel)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
