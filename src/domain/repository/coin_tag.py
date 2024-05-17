from abc import ABC, abstractmethod
from typing import Optional

from src.domain.enum.coin_tag_type import CoinTagType
from src.domain.model.coin_tag import CoinTag
from src.domain.repository.base import Repository


class CoinTagRepository(Repository[CoinTag], ABC):

    @abstractmethod
    def get_or_none_by_value(self, value: CoinTagType) -> Optional[CoinTag]:
        pass
