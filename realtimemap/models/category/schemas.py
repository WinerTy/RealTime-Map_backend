from pydantic import BaseModel, Field


class BaseCategory(BaseModel):
    category_name: str = Field(..., max_length=64)


class CreateCategory(BaseCategory):
    color: str = Field(..., max_length=32)


class UpdateCategory(CreateCategory):
    pass


class ReadCategory(BaseCategory):
    id: int
    icon: str
