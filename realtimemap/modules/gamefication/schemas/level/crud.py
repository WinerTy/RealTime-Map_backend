from typing import Optional

from pydantic import BaseModel, ConfigDict


class LevelRead(BaseModel):
    level: int
    required_exp: int
    color: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
