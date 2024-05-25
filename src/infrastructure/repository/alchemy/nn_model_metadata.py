from injector import inject

from src.domain.model.nn_model_metadata import NNModelMetadata
from src.domain.repository.nn_model_metadata import NNModelMetadataRepository
from src.infrastructure.repository.alchemy.base import AlchemyRepository
from src.infrastructure.repository.alchemy.engine import AlchemyEngine


class AlchemyNNModelMetadataRepository(AlchemyRepository[NNModelMetadata], NNModelMetadataRepository):
    @inject
    def __init__(self, engine: AlchemyEngine):
        super().__init__(engine, NNModelMetadata)
