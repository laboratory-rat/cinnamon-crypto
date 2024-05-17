import uuid
from datetime import datetime

import click
from ._injector import injector
from ...application.service.coin_pair import CoinPairService
from ...domain.schema.coin_pair import CoinPairDisplaySchema


def _display_all_pairs():
    application = injector.get(CoinPairService)
    pairs = application.get_all_short_display()

    def _schema_to_str(schema: CoinPairDisplaySchema, index: int) -> str:
        return f'{index:2}. [{schema.id}]\t{schema.base.symbol}/{schema.quote.symbol}'

    for index, pair in enumerate(pairs):
        click.echo(_schema_to_str(pair, index))


def _sync(pair: str):
    application = injector.get(CoinPairService)
    start_time = datetime.replace(datetime.now(), year=2022, month=1, day=1, hour=0, minute=0, second=0)
    end_time = datetime.replace(datetime.now(), hour=0, minute=0, second=0)
    application.fetch_coin_pair(pair_id=uuid.UUID(pair), start_timestamp=start_time.timestamp(), end_timestamp=end_time.timestamp(), period='1d', limit=500)


@click.command('pairs')
@click.option('--list', '-l', is_flag=True, help='List all available pairs')
@click.option('--sync', '-s', is_flag=True, help='Sync specified pair')
@click.argument('arg', type=str, required=False)
def pair_command(list: bool, sync: bool, arg: str):
    if list:
        _display_all_pairs()
        return

    if sync:
        if not arg:
            click.echo('No pair provided. Use --help to see available options')
            return

        _sync(arg)
        return

    click.echo('No command provided. Use --help to see available commands')
