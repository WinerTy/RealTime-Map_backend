from datetime import datetime, timezone
from typing import Optional, Union

from pydantic import Field, field_validator, model_validator, BaseModel

from models.user_ban.model import BanReason


class UserBanCreate(BaseModel):
    user_id: int
    moderator_id: int
    reason_text: Optional[str] = Field(
        ..., description="Sub reason text", max_length=256
    )
    reason: BanReason
    is_permanent: bool = Field(default=False, description="it's permanent ban?")
    banned_until: Optional[Union[str, datetime]] = Field(
        ..., description="banned until"
    )

    @field_validator("banned_until")
    def validate_banned_until(cls, v):
        if v is not None and v != "":
            if isinstance(v, str):
                v = datetime.fromisoformat(v)
            if v < datetime.now(timezone.utc):
                raise ValueError("Date must be in the future")
        return None

    @field_validator("reason_text")
    def validate_reason_text(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v

    @model_validator(mode="after")
    def validate_ban_duration(self) -> "UserBanCreate":
        """Валидация взаимосвязи is_permanent и banned_until"""
        if self.is_permanent and self.banned_until is not None:
            raise ValueError("For permanent bans, banned_until must be None")

        if not self.is_permanent and self.banned_until is None:
            raise ValueError("For banned until need same date")

        return self

    @model_validator(mode="after")
    def validate_reason_text_for_other(self) -> "UserBanCreate":
        """Валидация текста причины для 'other'"""
        if self.reason == BanReason.other and not self.reason_text:
            raise ValueError("For reason 'other' you must specify 'reason'")

        return self
