from abc import abstractmethod, ABC


class NNModuleRepository(ABC):
    @abstractmethod
    def save(self, model, model_name: str):
        raise NotImplementedError("Must override save")

    @abstractmethod
    def load(self, model_name: str):
        raise NotImplementedError("Must override load")

    @abstractmethod
    def all(self):
        raise NotImplementedError("Must override all")

    @abstractmethod
    def delete(self, model_name: str):
        raise NotImplementedError("Must override delete")