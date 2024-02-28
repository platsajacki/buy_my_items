from abc import ABCMeta, abstractmethod
from typing import Any


class BaseService(metaclass=ABCMeta):
    """Abstract base class for creating services."""
    def __call__(self) -> Any:
        """Calls the service to execute the business logic."""
        return self.act()

    @abstractmethod
    def act(self) -> Any:
        """Abstract method that must be implemented in the subclass. Contains the service's business logic."""
        raise NotImplementedError('Service is not implemented in the class.')
