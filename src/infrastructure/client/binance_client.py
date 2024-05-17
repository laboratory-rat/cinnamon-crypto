import datetime
import time
from typing import Literal, Tuple, List

from injector import inject
from pydantic import BaseModel, Field

from src.infrastructure.config.app_config import AppConfig
from binance.spot import Spot

from src.domain.helpers.time import interval_to_timedelta
from src.infrastructure.logger.app_logger import AppLogger


class ClientGetHistoricalKlinesProps(BaseModel):
    symbol: str
    interval: Literal['1h', '1d', '30m'] = '1h'
    start_time: float = (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
    end_time: float = Field(None, le=int(datetime.datetime.now().timestamp()))
    limit: int = Field(100, ge=1, le=1000)
    sleep_ms: int = Field(0, ge=0)


def split_timeline(start_time: float, end_time: float, interval: str, limit: int) -> List[Tuple[int, int]]:
    """ Split the timeline into chunks based on interval and limit. """
    # Convert timestamps to datetime
    start_time = datetime.datetime.fromtimestamp(start_time)
    end_time = datetime.datetime.fromtimestamp(end_time)

    # Parse the interval
    delta = interval_to_timedelta(interval)

    # Calculate total intervals
    total_time = end_time - start_time
    total_intervals = int(total_time / delta)

    # Calculate number of chunks
    num_chunks = (total_intervals + limit - 1) // limit

    # Generate the chunks
    chunks = []
    current_start = start_time

    for _ in range(num_chunks):
        current_end = current_start + delta * limit
        if current_end > end_time:
            current_end = end_time
        chunks.append((int(current_start.timestamp()), int(current_end.timestamp())))
        current_start = current_end

    return chunks


class ClientBinance:
    client_ = None
    logger: AppLogger

    @inject
    def __init__(self, config: AppConfig, logger: AppLogger):
        self.client_ = Spot(api_key=config.api_key, api_secret=config.api_secret)
        self.logger = logger

    @property
    def client(self):
        return self.client_

    def get_historical_klines_generator(self, props: ClientGetHistoricalKlinesProps):
        start_time = props.start_time
        end_time = props.end_time
        interval = props.interval
        limit = props.limit
        symbol = props.symbol
        sleep_ms = props.sleep_ms

        if not end_time:
            end_time = datetime.datetime.now().timestamp()

        start_time = int(start_time)
        end_time = int(end_time)
        self.logger.debug(f"Fetching data for {symbol} from {start_time} to {end_time} with interval {interval}")
        batches = split_timeline(start_time, end_time, interval, limit)
        # for start, end in batches:
        for start, end in batches:
            # TODO: Check up why it is not working with endTime
            result = self.client.klines(symbol, interval=interval, limit=limit, startTime=start) # Yes, startTime is camelCase
            yield result
            if sleep_ms > 0 and start != batches[-1][0]:
                time.sleep(sleep_ms / 1000)
