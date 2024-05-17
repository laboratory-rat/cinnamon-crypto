"""seed

Revision ID: 1
Revises: 0
Create Date: 2024-04-24 14:21:04.349530

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.domain.enum.coin_tag_type import CoinTagType
from src.domain.model.coin import Coin
from src.domain.model.coin_pair import CoinPair
from src.domain.model.coin_tag import CoinTag, CoinToTag
from migrations.to_seed_coins import coins_to_seed

# revision identifiers, used by Alembic.
revision = '1'
down_revision = '0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # add all tags
    all_tag_val = [val for val in CoinTagType.__members__.values()]
    for val in all_tag_val:
        session.add(CoinTag(value=val))

    session.commit()

    # add coins
    coin_symbol_to_data = {coin['symbol']: coin for coin in coins_to_seed}
    for _, data in coin_symbol_to_data.items():
        coin = session.query(Coin).filter_by(symbol=data['symbol']).first()
        if not coin:
            coin = Coin(name=data['name'], symbol=data['symbol'])
            session.add(coin)
            session.commit()

        for tag in data['tags']:
            tag_model = session.query(CoinTag).filter_by(value=tag).first()
            if not tag_model:
                tag_model = CoinTag(value=tag)
                session.add(tag_model)
                session.commit()

            tag_model.coins.append(coin)

        session.commit()

    # create all pairs combinations
    stable_coins = session.query(Coin).filter(Coin.tags.any(value=CoinTagType.STABLE)).all()
    non_stable_coins = session.query(Coin).filter(~Coin.tags.any(value=CoinTagType.STABLE)).all()

    for stable in stable_coins:
        for non_stable in non_stable_coins:
            pair = CoinPair(base_id=non_stable.id, quote_id=stable.id)
            session.add(pair)

    session.commit()


def downgrade() -> None:
    op.execute('DELETE FROM coin_to_tag')
    op.execute('DELETE FROM coin')
    op.execute('DELETE FROM coin_tag')
