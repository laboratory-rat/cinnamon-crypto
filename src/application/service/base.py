from abc import ABC
from typing import Type

from src.application.exception.base import AppException, AppNotFoundException
from src.infrastructure.logger.app_logger import AppLogger


class AppService(ABC):
    logger: AppLogger

    def __init__(self, logger: AppLogger):
        self.logger = logger

    def raise_exception(self, code: str, message: object, inner_exception: Exception = None):
        raise AppException(self.__class__, code, message, inner_exception)

    def raise_not_found(self, entity_type: Type, key: object, value: object, inner_exception: Exception = None):
        raise AppNotFoundException(self.__class__, entity_type, key, value, inner_exception)
