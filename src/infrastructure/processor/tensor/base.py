from abc import ABC, abstractmethod
from typing import List, Tuple, TypeVar, Generic

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler


Schema = TypeVar('Schema')


class BaseTensorProcessor(Generic[Schema], ABC):
    @abstractmethod
    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the scaler on the data and transform it.
        """
        raise NotImplementedError("Must override fit_transform")

    @abstractmethod
    def transform(self, schemas_list: List[Schema]) -> pd.DataFrame:
        """
        Transform the data using the fitted scaler.
        """
        raise NotImplementedError("Must override transform")

    @abstractmethod
    def create_sequences(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences from the data for LSTM input.
        """
        raise NotImplementedError("Must override create_sequences")

    @abstractmethod
    def to_tensor(self, x: np.ndarray, y: np.ndarray) -> (torch.Tensor, torch.Tensor):
        """
        Convert numpy arrays to PyTorch tensors.
        """
        raise NotImplementedError("Must override to_tensor")


class CandleDataTensorProcessor(BaseTensorProcessor):
    seq_length: int
    input_columns: List[str]
    output_columns: List[str]
    scaler: StandardScaler
    input_shape: Tuple[int, ...]
    output_shape: Tuple[int, ...]

    def __init__(self, seq_length: int, input_columns: list, output_columns: list, output_length: int):
        self.seq_length = seq_length
        self.input_columns = input_columns
        self.output_columns = output_columns
        self.scaler = StandardScaler()
        self.input_shape = (seq_length, len(input_columns))
        self.output_shape = (output_length, len(output_columns))

    def transform(self, schemas_list: List[Schema]) -> pd.DataFrame:
        """
        Transform the data into dataframe.
        """
        return pd.DataFrame(
            [schema.model_dump() for schema in schemas_list],
            columns=(self.input_columns + self.output_columns)
        )

    def fit_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the scaler on the data and transform it.
        """
        scaled_data = self.scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=(self.input_columns + self.output_columns))

    def split_sequences(self, arr: np.ndarray, split: Tuple[float, ...] = (.5, .5)) -> List[np.ndarray]:
        """
        Split the tensor into multiple tensors.
        """

        if sum(split) != 1:
            raise ValueError("Sum of split values must be 1.")

        return np.split(arr, [int(len(arr) * split_value) for split_value in split])

    def to_tensor(self, x: np.ndarray, y: np.ndarray) -> (torch.Tensor, torch.Tensor):
        """
        Convert numpy arrays to PyTorch tensors.
        """
        x_tensor = torch.tensor(x, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)
        return x_tensor, y_tensor

    def create_sequences(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences from the data for LSTM input.
        """
        only_input = data[self.input_columns]
        only_output = data[self.output_columns]

        xs = []
        ys = []

        for i in range(len(data) - self.seq_length - self.output_shape[0] + 1):
            x = only_input.iloc[i:(i + self.seq_length)].values
            y = only_output.iloc[(i + self.seq_length):(i + self.seq_length + self.output_shape[0])].values.flatten()

            xs.append(x)
            ys.append(y)

        return np.array(xs), np.array(ys)
