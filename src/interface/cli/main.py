import click
from .pair import pair_command


@click.group()
def cli():
    pass


@cli.command()
@click.option('--pair', '-p', help='Currency pair to fetch', required=False)
def fetch_currencies_pairs(pair: str):
    """Fetch all the available currencies pairs"""
    pass


cli.add_command(pair_command)
cli()