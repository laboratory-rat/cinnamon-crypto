from logging import Logger, getLogger

from injector import inject

from src.infrastructure.config.app_config import AppConfig


class AppLogger:
    logger_: Logger
    config: AppConfig

    @inject
    def __init__(self, config: AppConfig):
        self.config = config
        self.logger_ = self._set_default_logger()

    def debug(self, message: str):
        print(message)
        # self.logger_.debug(message)

    def info(self, message: str):
        print(message)
        # self.logger_.info(message)

    def warning(self, message: str):
        print(message)
        # self.logger_.warning(message)

    def error(self, message: str):
        print(message)
        # self.logger_.error(message)

    def _set_default_logger(self) -> Logger:
        logger = getLogger(__name__)
        logger.setLevel('DEBUG')
        return logger
