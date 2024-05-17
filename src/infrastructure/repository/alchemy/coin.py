from injector import inject

from src.domain.model.coin import Coin
from src.domain.repository.coin import CoinRepository
from src.infrastructure.repository.alchemy.base import AlchemyRepository
from src.infrastructure.repository.alchemy.engine import AlchemyEngine


class AlchemyCoinRepository(AlchemyRepository[Coin], CoinRepository):
    @inject
    def __init__(self, engine: AlchemyEngine):
        super().__init__(engine, Coin)
