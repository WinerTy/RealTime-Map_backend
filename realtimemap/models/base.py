from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import conf
from utils import camel_case_to_snake_case


class BaseSqlModel(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=conf.db.naming_convention)

    @classmethod
    def _validate_filter_fields(cls):
        pass

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)
