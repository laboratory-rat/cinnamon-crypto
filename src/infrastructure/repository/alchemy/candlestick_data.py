from injector import inject

from src.domain.model.candlestick_data import CandlestickData
from src.domain.repository.candlestick_data import CandlestickDataRepository
from src.infrastructure.repository.alchemy.base import AlchemyRepository
from src.infrastructure.repository.alchemy.engine import AlchemyEngine


class AlchemyCandlestickDataRepository(AlchemyRepository['CandlestickData'], CandlestickDataRepository):
    @inject
    def __init__(self, engine: AlchemyEngine):
        super().__init__(engine, CandlestickData)

