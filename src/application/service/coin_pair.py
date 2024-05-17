import uuid
from typing import Literal, List

from injector import inject

from src.domain.model.candlestick_data import CandlestickData
from src.domain.repository.candlestick_data import CandlestickDataRepository
from src.domain.repository.coin_pair import CoinPairRepository
from src.domain.repository.base import AppQuery, AppFilter, AppPagination
from src.domain.schema.candlestick_data import CandlestickDataSchema
from src.domain.schema.coin_pair import CoinPairDisplaySchema
from src.infrastructure.client.binance_client import ClientBinance, ClientGetHistoricalKlinesProps
from src.infrastructure.logger.app_logger import AppLogger


class CoinPairService:
    coin_pair_repository: CoinPairRepository
    candlestick_data_repository: CandlestickDataRepository
    client_binance: ClientBinance
    logger: AppLogger

    @inject
    def __init__(self, coin_pair_repository: CoinPairRepository, candlestick_data_repository: CandlestickDataRepository,
                 client_binance: ClientBinance, logger: AppLogger):
        self.coin_pair_repository = coin_pair_repository
        self.candlestick_data_repository = candlestick_data_repository
        self.client_binance = client_binance
        self.logger = logger

    def fetch_coin_pair(self, pair_id: uuid.UUID, start_timestamp: float, end_timestamp: float,
                        period: Literal['1h', '1d', '30m'] = '1h', sleep=2000, limit=100):
        pair = self.coin_pair_repository.get(pair_id)
        if not pair:
            raise ValueError(f"Pair with id {pair_id} does not exist")

        # time to closest 30min
        start_timestamp = start_timestamp - start_timestamp % 1800
        end_timestamp = end_timestamp - end_timestamp % 1800
        props = ClientGetHistoricalKlinesProps(symbol=pair.pair_str, interval=period, start_time=start_timestamp,
                                               end_time=end_timestamp, sleep_ms=sleep, limit=limit)
        for result_batch in self.client_binance.get_historical_klines_generator(props):
            self.logger.debug(f"Received {len(result_batch)} results")
            for result in result_batch:
                schema = CandlestickDataSchema.from_binance_data(pair.id, result)
                # filter if already exists
                query_filter = AppQuery(
                    filters=[AppFilter.create(lambda x: x.open_time == schema.open_time)],
                    pagination=AppPagination(limit=1),
                )
                existing = self.candlestick_data_repository.find(query_filter)
                if existing and len(existing) > 0:
                    self.logger.debug(f"Data already exists for {schema.open_time}")
                    continue

                self.logger.debug(f"Adding new candlestick data {schema.open_time}")
                candlestick_data: CandlestickData = CandlestickData(**schema.model_dump())
                self.candlestick_data_repository.add(candlestick_data)

    def get_all_short_display(self) -> List[CoinPairDisplaySchema]:
        all_pairs = self.coin_pair_repository.get_all()
        return [CoinPairDisplaySchema.model_validate(pair) for pair in all_pairs]
