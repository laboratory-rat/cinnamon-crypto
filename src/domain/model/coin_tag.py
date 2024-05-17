import datetime
from typing import List

from sqlalchemy import ForeignKey, Table, Column, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.domain.enum.coin_tag_type import CoinTagType
from src.domain.model.entity import AppEntity


CoinToTag = Table(
    'coin_to_tag',
    AppEntity.metadata,
    Column('coin_id', ForeignKey('coin.id'), primary_key=True),
    Column('tag_id', ForeignKey('coin_tag.id'), primary_key=True),
    Column('created_at', DateTime, nullable=False, default=datetime.datetime.utcnow),
)


class CoinTag(AppEntity):
    __tablename__ = 'coin_tag'

    value: Mapped[CoinTagType] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(nullable=False, default='binance')

    coins: Mapped[List['Coin']] = relationship(secondary='coin_to_tag', back_populates='tags')
