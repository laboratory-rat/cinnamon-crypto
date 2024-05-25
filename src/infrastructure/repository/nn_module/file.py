import os
from typing import List

import torch
from injector import inject

from src.domain.repository.nn_module import NNModuleRepository
from src.infrastructure.config.app_config import AppConfig


class FileNNModuleRepository(NNModuleRepository):
    base_folder: str

    @inject
    def __init__(self, app_config: AppConfig):
        self.base_folder = app_config.nn.path
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

    def save(self, model, model_name: str):
        torch.save(model, f"{self.base_folder}/{model_name}.pt")

    def load(self, model_name: str):
        return torch.load(f"{self.base_folder}/{model_name}.pt")

    def all(self) -> List[str]:
        models_list = []
        for model in [item for item in os.listdir(self.base_folder) if item.endswith(".pt")]:
            models_list.append(model.replace(".pt", ""))

        return models_list

    def delete(self, model_name: str):
        os.remove(f"{self.base_folder}/{model_name}.pt")
