from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface für Speicheradapter (WAS, nicht WIE).
    """

    @abstractmethod
    def load_habits(self):
        pass

    @abstractmethod
    def save_habits(self, habits):
        pass