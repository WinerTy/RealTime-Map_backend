from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schemas_request import MessageParamsRequest


@dataclass(frozen=True)
class MessageFilter:
    before: datetime
    limit: int = 50

    @classmethod
    def from_request(cls, req: "MessageParamsRequest") -> "MessageFilter":
        return cls(
            before=req.before,
            limit=req.limit,
        )
