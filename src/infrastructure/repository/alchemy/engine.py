from injector import inject
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.infrastructure.config.app_config import AppConfig


class AlchemyEngine:
    maker = None

    @inject
    def __init__(self, app_config: AppConfig):
        self._engine = create_engine(app_config.database.connection_string)
        self.maker = sessionmaker(bind=self._engine)

    def create_session(self) -> Session:
        return self.maker()
