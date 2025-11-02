from abc import ABC, abstractmethod


class BaseLoader(ABC):
    """Abstract base class for file loaders."""

    @abstractmethod
    def load_data(self):
        pass
