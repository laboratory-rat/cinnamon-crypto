import uuid

from pydantic import ConfigDict

from src.domain.schema.base import BaseEntitySchema


class CandlestickDataSchema(BaseEntitySchema):
    model_config = ConfigDict(from_attributes=True)

    open_time: int
    close_time: int
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float
    coin_pair_id: uuid.UUID

    @classmethod
    def from_binance_data(cls, coin_pair_id: uuid.UUID, raw_data: list) -> 'CandlestickDataSchema':
        return cls(
            open_time=int(raw_data[0]),
            close_time=int(raw_data[6]),
            open_price=float(raw_data[1]),
            high_price=float(raw_data[2]),
            low_price=float(raw_data[3]),
            close_price=float(raw_data[4]),
            volume=float(raw_data[5]),
            quote_asset_volume=float(raw_data[7]),
            number_of_trades=int(raw_data[8]),
            taker_buy_base_asset_volume=float(raw_data[9]),
            taker_buy_quote_asset_volume=float(raw_data[10]),
            coin_pair_id=coin_pair_id,
        )
