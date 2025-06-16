from pydantic import BaseModel, Field, field_validator


class BaseMarkComment(BaseModel):
    content: str = Field(..., description="Mark content", min_length=1)

    @field_validator("content", mode="before")
    @classmethod
    def validate_content(cls, value: str):
        if len(value) > 256:
            raise ValueError("Mark content must be less than 256 characters")

        return value


class CreateMarkComment(BaseMarkComment):
    mark_id: int = Field(..., description="Mark id", ge=0)
    user_id: int = Field(..., description="User id", ge=0)


class UpdateMarkComment(CreateMarkComment):
    likes: int = Field(..., description="Likes", ge=0)
    dislikes: int = Field(..., description="Dislikes", ge=0)


class ReadMarkComment(BaseMarkComment):
    mark_id: int = Field(..., description="Mark id", ge=0)
    likes: int = Field(..., description="Likes", ge=0)
    dislikes: int = Field(..., description="Dislikes", ge=0)


class CreateMarkCommentRequest(BaseMarkComment):
    pass
