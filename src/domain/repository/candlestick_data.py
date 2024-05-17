from abc import ABC

from src.domain.model.candlestick_data import CandlestickData
from src.domain.repository.base import Repository


class CandlestickDataRepository(Repository[CandlestickData], ABC):
    pass
