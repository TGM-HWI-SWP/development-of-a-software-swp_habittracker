from myapp.contracts.storage_interface import StorageInterface

class MockStorage(StorageInterface):
    """
    Mock-Speicher für Tests und GUI-Dummy-Daten.
    Keine echte Datei, sondern nur In-Memory-Dictionary.
    """

    def __init__(self):
        self._data = {
            "habits": [
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
        }

    def load_data(self) -> dict:
        return self._data

    def save_data(self, data: dict) -> None:
        self._data = data
