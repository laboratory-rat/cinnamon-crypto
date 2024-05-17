import uuid
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.domain.model.entity import AppEntity


class CoinPair(AppEntity):
    __tablename__ = "coin_pair"

    base_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('coin.id'), nullable=False)
    quote_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('coin.id'), nullable=False)

    candlestick_data: Mapped[List['CandlestickData']] = relationship(back_populates="coin_pair")
    base: Mapped['Coin'] = relationship(back_populates="base_pairs", foreign_keys=[base_id])
    quote: Mapped['Coin'] = relationship(back_populates="quote_pairs", foreign_keys=[quote_id])

    def __str__(self):
        return f"{self.base}/{self.quote}"

    @property
    def pair_str(self) -> str:
        return f"{self.base.symbol}{self.quote.symbol}"
