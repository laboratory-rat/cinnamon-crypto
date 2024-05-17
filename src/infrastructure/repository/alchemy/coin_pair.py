from typing import Type

from injector import inject

from src.domain.model.coin_pair import CoinPair
from src.domain.repository.coin_pair import CoinPairRepository
from src.infrastructure.repository.alchemy.base import AlchemyRepository
from src.infrastructure.repository.alchemy.engine import AlchemyEngine


class AlchemyCoinPairRepository(AlchemyRepository[Type[CoinPair]], CoinPairRepository):
    @inject
    def __init__(self, engine: AlchemyEngine):
        super().__init__(engine, CoinPair)
