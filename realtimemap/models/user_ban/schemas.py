from datetime import datetime, timezone, timedelta
from typing import Optional, Union, Annotated

from pydantic import Field, field_validator, model_validator, BaseModel

from models.user_ban.model import BanReason


class UserBanCreate(BaseModel):
    user_id: Annotated[int, Field(description="User ID to ban")]
    moderator_id: Annotated[int, Field(description="Moderator ID who issues the ban")]
    reason_text: Annotated[
        Optional[str], Field(None, description="Sub reason text", max_length=256)
    ]
    reason: Annotated[BanReason, Field(description="Ban reason")]
    is_permanent: Annotated[bool, Field(False, description="Is it a permanent ban?")]
    banned_until: Annotated[
        Optional[Union[str, datetime]], Field(None, description="Banned until date")
    ]

    @field_validator("banned_until")
    @classmethod
    def validate_banned_until(cls, v):
        if v is not None and v != "":
            if isinstance(v, str):
                v = datetime.fromisoformat(v)
            if v < datetime.now():
                raise ValueError("Date must be in the future")
            return v
        return None

    @field_validator("reason_text")
    @classmethod
    def validate_reason_text(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v

    @model_validator(mode="after")
    def validate_ban_duration(self) -> "UserBanCreate":
        """Validate the relationship between is_permanent and banned_until"""
        if self.is_permanent and self.banned_until is not None:
            raise ValueError("For permanent bans, banned_until must be None")

        if not self.is_permanent and self.banned_until is None:
            raise ValueError("For temporary bans, banned_until must be specified")

        return self

    @model_validator(mode="after")
    def validate_reason_text_for_other(self) -> "UserBanCreate":
        """Validate reason text for 'other' reason"""
        if self.reason == BanReason.other and not self.reason_text:
            raise ValueError("For reason 'other', you must specify 'reason_text'")

        return self
