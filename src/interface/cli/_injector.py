from injector import Injector

from src.infrastructure.config.app_config import AppConfig
from src.application.di import AppModule

config = AppConfig()
injector = Injector([AppModule(config)])
