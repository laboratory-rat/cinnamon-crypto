import uuid

from pydantic import BaseModel, ConfigDict

from src.domain.schema.candlestick_data import CandlestickDataSchema
from src.domain.schema.coin import CoinDisplaySchema


class CoinPairDisplaySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    base: CoinDisplaySchema
    quote: CoinDisplaySchema

    created_at: float
    updated_at: float


class CoinPairWithCandlestickDataSchema(CoinPairDisplaySchema):
    model_config = ConfigDict(from_attributes=True)

    candlestick_data: list[CandlestickDataSchema]
