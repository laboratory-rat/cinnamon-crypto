import uuid

from injector import inject
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import random_split, TensorDataset, DataLoader

from src.application.processor.nn_model import NNModelProcessor
from src.application.service.base import AppService
from src.application.service.candlestick_data import CandlestickDataService
from src.application.service.coin_pair import CoinPairService
from src.domain.repository.nn_module import NNModuleRepository
from src.infrastructure.learn.lstm_first import InstanceLSTMFirstModule
from src.infrastructure.logger.app_logger import AppLogger
from src.infrastructure.processor.tensor.base import CandleDataTensorProcessor


class TrainingService(AppService):
    candlestick_data_service: CandlestickDataService
    coin_pair_service: CoinPairService
    nn_module_repository: NNModuleRepository

    @inject
    def __init__(self, candlestick_data_service: CandlestickDataService, coin_pair_service: CoinPairService, nn_module_repository: NNModuleRepository, logger: AppLogger):
        super().__init__(logger)
        self.candlestick_data_service = candlestick_data_service
        self.coin_pair_service = coin_pair_service
        self.nn_module_repository = nn_module_repository

    def train_from_coin_pair(self, coin_pair: uuid.UUID, model_name: str):
        coin_pair = self.coin_pair_service.get_by_id(coin_pair)
        candlestick_total_data = self.candlestick_data_service.count_by_coin_pair(coin_pair.id)
        candlestick_data = self.candlestick_data_service.filter_by_coin_pair(coin_pair.id, limit=candlestick_total_data)

        seq_length = 14
        output_length = 4
        tensor_processor = CandleDataTensorProcessor(
            seq_length,
            ['open_price', 'high_price', 'low_price', 'volume', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume'],
            ['close_price'],
            4,
        )
        model_to_train = InstanceLSTMFirstModule(
            input_size=len(tensor_processor.input_columns),
            output_size=output_length,
        )

        raw_data = tensor_processor.transform(candlestick_data)
        scaled_data = tensor_processor.fit_transform(raw_data)

        x, y = tensor_processor.create_sequences(scaled_data)
        x_tensor, y_tensor = tensor_processor.to_tensor(x, y)
        dataset = TensorDataset(x_tensor, y_tensor)
        train_size = int(0.7 * len(dataset))
        val_size = int(0.15 * len(dataset))
        test_size = len(dataset) - train_size - val_size
        train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=False)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

        processor = NNModelProcessor(logger=self.logger, model=model_to_train, lr=0.001)
        processor.fit(train_loader, val_loader, num_epochs=1000, verbose=10)
        test_result = processor.evaluate(test_loader)

        for inputs, targets in test_loader:
            test_result_raw = processor.execute(inputs)
            self.logger.info(f'Test result: {test_result_raw.cpu().numpy()}\texpected: {targets.cpu().numpy()}')

        self.logger.info(f'Test result: {test_result:.4}')
        self.nn_module_repository.save(model_to_train, model_name)
