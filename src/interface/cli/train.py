import uuid

import click
from ._injector import injector
from ...application.service.training import TrainingService


@click.command('train')
@click.option('--pair', '-p', type=str, help='Train model from specified pair')
def train_command(pair: str):
    click.echo(f"Training model from pair {pair}")
    pair_id = uuid.UUID(pair)

    application = injector.get(TrainingService)
    application.train_from_coin_pair(pair_id, model_name='test_model')
