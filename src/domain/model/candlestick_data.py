import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.model.entity import AppEntity


class CandlestickData(AppEntity):
    __tablename__ = "candlestick_data"

    open_time: Mapped[int] = mapped_column(nullable=False)
    close_time: Mapped[int] = mapped_column(nullable=False)
    open_price: Mapped[float] = mapped_column(nullable=False)
    high_price: Mapped[float] = mapped_column(nullable=False)
    low_price: Mapped[float] = mapped_column(nullable=False)
    close_price: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float] = mapped_column(nullable=False)
    quote_asset_volume: Mapped[float] = mapped_column(nullable=False)
    number_of_trades: Mapped[int] = mapped_column(nullable=False)
    taker_buy_base_asset_volume: Mapped[float] = mapped_column(nullable=False)
    taker_buy_quote_asset_volume: Mapped[float] = mapped_column(nullable=False)

    coin_pair_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('coin_pair.id'), nullable=False)
    coin_pair: Mapped['CoinPair'] = relationship(back_populates="candlestick_data")

    def __str__(self):
        return f"{self.coin_pair.pair_str} {self.open_time} {self.close_time} {self.open_price} {self.high_price} {self.low_price} {self.close_price} {self.volume} {self.quote_asset_volume} {self.number_of_trades} {self.taker_buy_base_asset_volume} {self.taker_buy_quote_asset_volume}"
