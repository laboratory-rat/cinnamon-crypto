from abc import ABC
from typing import Type

from src.domain.model.coin_pair import CoinPair
from src.domain.repository.base import Repository


class CoinPairRepository(Repository[Type[CoinPair]], ABC):
    model_type: Type[CoinPair] = CoinPair
