from abc import ABC, abstractmethod

class Selector(ABC):
    @abstractmethod
    def select(self, configs, nframe):
        ...


