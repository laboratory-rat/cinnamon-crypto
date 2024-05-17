from abc import ABC

from src.domain.model.coin import Coin
from src.domain.repository.base import Repository


class CoinRepository(Repository[Coin], ABC):
    pass
