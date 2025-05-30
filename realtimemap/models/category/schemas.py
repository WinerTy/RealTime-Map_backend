from pydantic import BaseModel, Field, computed_field


class BaseCategory(BaseModel):
    category_name: str = Field(..., max_length=64)


class CreateCategory(BaseCategory):
    color: str = Field(..., max_length=32)


class UpdateCategory(CreateCategory):
    pass


class ReadCategory(BaseCategory):
    id: int
    icon: str

    @computed_field
    @property
    def len_name(self) -> int:
        return len(self.category_name)
