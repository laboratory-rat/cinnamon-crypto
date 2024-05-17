import uuid
from typing import List

from pydantic import BaseModel, ConfigDict


class CoinTagSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    value: str


class CoinDisplaySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    symbol: str
    tags: List[CoinTagSchema]
