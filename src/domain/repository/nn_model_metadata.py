from abc import ABC

from src.domain.model.nn_model_metadata import NNModelMetadata
from .base import Repository


class NNModelMetadataRepository(Repository[NNModelMetadata], ABC):
    pass
