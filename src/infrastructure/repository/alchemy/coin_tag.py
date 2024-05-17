from typing import Optional

from injector import inject

from src.domain.enum.coin_tag_type import CoinTagType
from src.domain.model.coin_tag import CoinTag
from src.domain.repository.coin_tag import CoinTagRepository
from src.infrastructure.repository.alchemy.base import AlchemyRepository
from src.infrastructure.repository.alchemy.engine import AlchemyEngine


class AlchemyCoinTagRepository(AlchemyRepository[CoinTag], CoinTagRepository):
    @inject
    def __init__(self, engine: AlchemyEngine):
        super().__init__(engine, CoinTag)

    def get_or_none_by_value(self, value: CoinTagType) -> Optional[CoinTag]:
        return self.session.query(self.entity_class).filter(CoinTag.value == value).one_or_none()
