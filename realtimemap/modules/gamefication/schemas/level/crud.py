from pydantic import BaseModel, ConfigDict


class LevelRead(BaseModel):
    level: int
    required_exp: int

    model_config = ConfigDict(from_attributes=True)
