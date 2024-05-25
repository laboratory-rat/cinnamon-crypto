import uuid
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List, Callable, Any, Literal, Type

Entity = TypeVar('Entity')


class AppFilter(Generic[Entity]):
    condition: Callable[[Entity], bool]

    def __init__(self, condition: Callable[[Entity], bool]):
        self.condition = condition

    @classmethod
    def create(cls, condition: Callable[[Entity], bool]) -> 'AppFilter[Entity]':
        return cls(condition)


class AppOrder(Generic[Entity]):
    param: str | Any
    direction: Literal['asc', 'desc']

    def __init__(self, param: str | Any, direction: Literal['asc', 'desc'] = 'asc'):
        if direction not in ['asc', 'desc']:
            raise ValueError('Direction must be either "asc" or "desc"')

        self.param = param
        self.direction = direction

    @classmethod
    def create(cls, param: str | Any, direction: Literal['asc', 'desc'] = 'asc') -> 'AppOrder[Entity]':
        return cls(param, direction)


class AppPagination(Generic[Entity]):
    skip: int = 0
    limit: int = 100

    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = max(skip, 0)
        self.limit = max(limit, 1)

    @classmethod
    def create(cls, skip: int = 0, limit: int = 100) -> 'AppPagination[Entity]':
        return cls(skip, limit)


class AppQuery(Generic[Entity]):
    filters: List[AppFilter[Entity]] | AppFilter[Entity] = None
    orders: List[AppOrder[Entity]] | AppOrder[Entity] = None
    pagination: AppPagination[Entity] = None

    def __init__(self, filters: List[AppFilter[Entity]] | AppFilter[Entity] = None,
                 orders: List[AppOrder[Entity]] | AppOrder[Entity] = None, pagination: AppPagination[Entity] = None):
        self.filters = filters
        self.orders = orders
        self.pagination = pagination


class Repository(Generic[Entity], ABC):
    model_type: Type[Entity]

    @abstractmethod
    def add(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    def get(self, id: uuid.UUID) -> Optional[Entity]:
        pass

    @abstractmethod
    def get_by_filter(self, filter_obj: AppQuery[Entity]) -> Optional[Entity]:
        pass

    @abstractmethod
    def find(self, filter_obj: AppQuery[Entity]) -> List[Entity]:
        pass

    @abstractmethod
    def get_all(self) -> List[Entity]:
        pass

    @abstractmethod
    def count(self, filter_obj: AppQuery[Entity] = None) -> int:
        pass

    @abstractmethod
    def update(self, entity: Entity) -> Entity:
        pass

    @abstractmethod
    def delete(self, entity: Entity) -> Entity:
        pass
