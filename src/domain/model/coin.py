from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .entity import AppEntity


class Coin(AppEntity):
    __tablename__ = "coin"

    name: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str] = mapped_column(nullable=False)

    base_pairs: Mapped[List['CoinPair']] = relationship(back_populates="base", foreign_keys="CoinPair.base_id")
    quote_pairs: Mapped[List['CoinPair']] = relationship(back_populates="quote", foreign_keys="CoinPair.quote_id")
    tags: Mapped[List['CoinTag']] = relationship(secondary='coin_to_tag', back_populates="coins")

    @property
    def tags_str(self) -> List[str]:
        return [tag.name for tag in self.tags]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id} {self.name} {self.symbol}>"
