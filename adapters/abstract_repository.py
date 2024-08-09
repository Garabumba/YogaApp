import abc
from typing import TypeVar

T = TypeVar('T')

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: T):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, **kwargs) -> T:
        raise NotImplementedError