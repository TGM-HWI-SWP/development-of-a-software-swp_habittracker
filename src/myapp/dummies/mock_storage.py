from myapp.contracts.storage_interface import IStorage


class MockStorage(IStorage):
    """
    In-Memory-Storage für MVP / Prototyp.
    """

    def __init__(self):
        self._habits = [
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
                "description": "10 Seiten lesen",
                "frequency": "daily",
                "is_done_today": False
            }
        ]

    def load_habits(self):
        return self._habits

    def save_habits(self, habits):
        self._habits = habits
