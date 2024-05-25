import uuid
from typing import List, Literal

from injector import inject

from src.application.service.base import AppService
from src.domain.repository.base import AppQuery, AppFilter, AppOrder, AppPagination
from src.domain.repository.candlestick_data import CandlestickDataRepository
from src.domain.schema.candlestick_data import CandlestickDataSchema
from src.infrastructure.logger.app_logger import AppLogger


class CandlestickDataService(AppService):
    candlestick_data_repository: CandlestickDataRepository

    @inject
    def __init__(self, candlestick_data_repository: CandlestickDataRepository, logger: AppLogger):
        super().__init__(logger)
        self.candlestick_data_repository = candlestick_data_repository

    def count_by_coin_pair(self, coin_pair_id: uuid.UUID) -> int:
        return self.candlestick_data_repository.count(AppQuery(filters=[AppFilter.create(lambda x: x.coin_pair_id == coin_pair_id)]))

    def filter_by_coin_pair(self,
                            coin_pair_id: uuid.UUID,
                            limit: int = 100,
                            start_time: int = None,
                            order_prop: str = 'open_time',
                            order_direction: Literal['asc', 'desc'] = 'asc',
                            ) -> List[CandlestickDataSchema]:
        query = AppQuery(
            filters=[AppFilter.create(lambda x: x.coin_pair_id == coin_pair_id)],
            orders=[AppOrder.create(order_prop, order_direction)],
            pagination=AppPagination(limit=limit),
        )

        if start_time:
            query.filters.append(AppFilter.create(lambda x: x.open_time >= start_time))

        models = self.candlestick_data_repository.find(query)
        return [CandlestickDataSchema.model_validate(model) for model in models]
