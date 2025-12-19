from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IStorage(ABC):
    """
    Interface für persistente Speicheradapter.
    Definiert NUR die Schnittstelle (WAS).
    """

    @abstractmethod
    def load_habits(self) -> List[Dict[str, Any]]:
        """Lädt alle Habits."""
        raise NotImplementedError

    @abstractmethod
    def save_habits(self, habits: List[Dict[str, Any]]) -> None:
        """Speichert alle Habits."""
        raise NotImplementedError
