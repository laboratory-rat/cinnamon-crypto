from injector import Module, singleton

from src.application.service.candlestick_data import CandlestickDataService
from src.application.service.coin_pair import CoinPairService
from src.infrastructure.config.app_config import AppConfig
from src.domain.repository.candlestick_data import CandlestickDataRepository
from src.domain.repository.coin import CoinRepository
from src.domain.repository.coin_pair import CoinPairRepository
from src.domain.repository.coin_tag import CoinTagRepository
from src.infrastructure.client.binance_client import ClientBinance
from src.infrastructure.logger.app_logger import AppLogger
from src.infrastructure.repository.alchemy.candlestick_data import AlchemyCandlestickDataRepository
from src.infrastructure.repository.alchemy.coin import AlchemyCoinRepository
from src.infrastructure.repository.alchemy.coin_pair import AlchemyCoinPairRepository
from src.infrastructure.repository.alchemy.coin_tag import AlchemyCoinTagRepository
from src.infrastructure.repository.alchemy.engine import AlchemyEngine


class AppModule(Module):
    config: AppConfig

    def __init__(self, config: AppConfig):
        self.config = config

    def configure(self, binder):
        # config
        binder.bind(AppConfig, self.config, scope=singleton)

        # logger
        binder.bind(AppLogger, to=AppLogger, scope=singleton)

        # repositories
        binder.bind(AlchemyEngine, AlchemyEngine)
        binder.bind(CoinRepository, AlchemyCoinRepository, scope=singleton)
        binder.bind(CoinTagRepository, AlchemyCoinTagRepository, scope=singleton)
        binder.bind(CoinPairRepository, AlchemyCoinPairRepository, scope=singleton)
        binder.bind(CandlestickDataRepository, AlchemyCandlestickDataRepository, scope=singleton)

        # clients
        binder.bind(ClientBinance, ClientBinance, scope=singleton)

        # applications
        binder.bind(CoinPairService, CoinPairService)
        binder.bind(CandlestickDataService, CandlestickDataService)
