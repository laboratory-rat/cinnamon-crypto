import time
from typing import Callable, List, Literal

import torch
import torch.optim as optim
import torch.nn as nn
from injector import inject
from pydantic import BaseModel
from torch.utils.data import DataLoader

from src.infrastructure.logger.app_logger import AppLogger


class NNModelProcessorCallbackMetadata(BaseModel):
    type: Literal['train', 'validation']
    epoch: int
    num_epochs: int
    loss: float
    epoch_loss: float
    epoch_time: float


class NNModelProcessor:
    logger: AppLogger
    model: torch.nn.Module
    criterion: torch.nn.Module
    optimizer: torch.optim.Optimizer

    callback: Callable[[NNModelProcessorCallbackMetadata], None]

    @inject
    def __init__(self,
                 logger: AppLogger,
                 model: torch.nn.Module,
                 criterion=nn.MSELoss(),
                 optimizer=None,
                 lr=0.001,
                 callback: Callable[[NNModelProcessorCallbackMetadata], None] = None
                 ):
        self.logger = logger
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer if optimizer else optim.Adam(self.model.parameters(), lr=lr)
        self.callback = callback if callback else self._default_callback

    def fit(self, train_loader: DataLoader, val_loader: DataLoader = None, num_epochs=100, verbose=10) -> List[NNModelProcessorCallbackMetadata]:
        result = []
        loss = 0.0

        for epoch in range(num_epochs):
            epoch_start_time = time.time()
            self.model.train()
            running_loss = 0.0

            for inputs, targets in train_loader:
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()

            epoch_loss = running_loss / len(train_loader)

            if val_loader is not None:
                loss = self.evaluate(val_loader)
                result.append(NNModelProcessorCallbackMetadata(
                    type='validation', epoch=epoch, num_epochs=num_epochs, loss=loss, epoch_loss=epoch_loss,
                    epoch_time=time.time() - epoch_start_time))
            else:
                result.append(NNModelProcessorCallbackMetadata(
                    type='train',
                    epoch=epoch, num_epochs=num_epochs, loss=loss.item(), epoch_loss=epoch_loss,
                    epoch_time=time.time() - epoch_start_time))

            if (epoch + 1) % verbose == 0:
                self.callback(result[-1])

        return result

    def evaluate(self, data_loader: DataLoader) -> float:
        self.model.eval()
        running_loss = 0.0
        with torch.no_grad():
            for inputs, targets in data_loader:
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                running_loss += loss.item()

        avg_loss = running_loss / len(data_loader)
        return avg_loss

    def execute(self, x: torch.Tensor) -> torch.Tensor:
        self.model.eval()
        with torch.no_grad():
            return self.model(x)

    def _default_callback(self, metadata: NNModelProcessorCallbackMetadata):
        epoch = metadata.epoch
        num_epochs = metadata.num_epochs
        loss = metadata.loss
        spend_time = metadata.epoch_time
        epoch_loss = metadata.epoch_loss

        if (epoch + 1) % 10 == 0:
            self.logger.info(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss:.4f}, Epoch Loss: {epoch_loss:.4f} in {spend_time:.2f} seconds')
