from sqlalchemy import TypeDecorator, VARCHAR

from src.domain.enum.coin_tag_type import CoinTagType


class CoinTagTypeDecorator(TypeDecorator):
    """Platform-independent CoinTagType type."""
    impl = VARCHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(VARCHAR(50))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return CoinTagType(value)
