from typing import Optional, Annotated

from pydantic import Field

from .crud import BaseComment


class CreateCommentRequest(BaseComment):
    parent_id: Annotated[
        Optional[int], Field(None, description="Parent comment id", ge=1)
    ]
