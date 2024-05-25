from typing import Tuple

from sqlalchemy.orm import Mapped

from src.domain.model.entity import AppEntity


class NNModelMetadata(AppEntity):
    __tablename__ = 'nn_model_metadata'

    name: Mapped[str]
    version_major: Mapped[str]
    version_minor: Mapped[str]
    version_patch: Mapped[str]
    description: Mapped[str] = None
    link: Mapped[str] = None

    input_columns: Mapped[str]
    input_shape: Mapped[str]
    output_shape: Mapped[str]

    @property
    def version(self) -> str:
        return f"{self.version_major}.{self.version_minor}.{self.version_patch}"

    def set_version(self, version: str):
        self.version_major, self.version_minor, self.version_patch = version.split(".")

    @property
    def input_shape_size(self) -> Tuple[int, ...]:
        return tuple(map(int, self.input_shape.split(",")))

    @input_shape_size.setter
    def input_shape_size(self, value: Tuple[int, ...]):
        self.input_shape = ",".join(map(str, value))

    @property
    def output_shape_size(self) -> Tuple[int, ...]:
        return tuple(map(int, self.output_shape.split(",")))

    @output_shape_size.setter
    def output_shape_size(self, value: Tuple[int, ...]):
        self.output_shape = ",".join(map(str, value))

    @property
    def input_columns_list(self) -> Tuple[str, ...]:
        return tuple(self.input_columns.split(","))

    @input_columns_list.setter
    def input_columns_list(self, value: Tuple[str, ...]):
        self.input_columns = ",".join(value)
