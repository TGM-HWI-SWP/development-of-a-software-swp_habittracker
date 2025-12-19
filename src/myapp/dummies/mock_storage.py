from typing import List, Dict, Any
from myapp.contracts.storage_interface import IStorage


class MockStorage(IStorage):
    """
    In-Memory-Speicher für MVP & Tests.
    Simuliert eine echte Datenbank.
    """

    def __init__(self):
        self._habits: List[Dict[str, Any]] = [
            {
                "name": "Wasser trinken",
                "description": "Mindestens 2 Liter pro Tag",
                "frequency": "daily",
                "is_done_today": False
            },
            {
                "name": "Spazieren gehen",
                "description": "30 Minuten Gehzeit",
                "frequency": "daily",
                "is_done_today": True
            },
            {
                "name": "Lesen",
                "description": "Jeden Tag 10 Seiten",
                "frequency": "daily",
                "is_done_today": False
            }
        ]

    def load_habits(self) -> List[Dict[str, Any]]:
        return self._habits

    def save_habits(self, habits: List[Dict[str, Any]]) -> None:
        self._habits = habits
