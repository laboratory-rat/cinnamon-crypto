import uuid
from typing import TypeVar, List, Optional, Type

from sqlalchemy import desc, asc

from src.domain.model.entity import AppEntity
from src.domain.repository.base import Repository
from src.domain.repository.base import AppQuery
from src.infrastructure.repository.alchemy.engine import AlchemyEngine

Entity = TypeVar('Entity', bound=AppEntity)


class AlchemyRepository(Repository[Entity]):
    def __init__(self, engine: AlchemyEngine, entity_class: Type[Entity]):
        self.session = engine.create_session()
        self.entity_class = entity_class

    def get(self, entity_id: uuid) -> Optional[Entity]:
        return self.session.query(self.entity_class).filter_by(id=entity_id).one_or_none()

    def get_by_filter(self, filter_obj: AppQuery[Entity]) -> Optional[Entity]:
        query = self.session.query(self.entity_class)
        query = self._apply_app_query(query, filter_obj)
        return query.one_or_none()

    def find(self, filter_obj: AppQuery[Entity]) -> List[Entity]:
        query = self.session.query(self.entity_class)
        query = self._apply_app_query(query, filter_obj)
        return query.all()

    def get_all(self) -> List[Entity]:
        return self.session.query(self.entity_class).filter_by().all()

    def count(self, filter_obj: AppQuery[Entity] = None) -> int:
        query = self.session.query(self.entity_class)
        query = self._apply_app_query(query, filter_obj, skip_pagination=True)
        return query.count()

    def add(self, entity: Entity) -> Entity:
        self.session.add(entity)
        self.session.commit()
        return entity

    def update(self, entity: Entity) -> Entity:
        self.session.add(entity)
        self.session.commit()
        return entity

    def delete(self, entity: Entity) -> Entity:
        self.session.delete(entity)
        self.session.commit()
        return entity

    def _apply_app_query(self, query, app_query: AppQuery = None, skip_pagination=False):
        if not app_query:
            return query

        app_filter = app_query.filters
        app_orders = app_query.orders
        app_pagination = app_query.pagination if not skip_pagination else None

        if app_filter:
            app_filter = app_filter if isinstance(app_filter, list) else [app_filter]
            for filter_ in app_filter:
                query = query.filter(filter_.condition(self.entity_class))

        if app_orders:
            app_orders = app_orders if isinstance(app_orders, list) else [app_orders]
            for order in app_orders:
                sql_alchemy_order = desc if order.direction == 'desc' else asc
                query = query.order_by(sql_alchemy_order(order.param))

        if app_pagination:
            query = query.limit(app_pagination.limit).offset(app_pagination.skip)

        return query
