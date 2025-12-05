from myapp.contracts.storage_interface import StorageInterface
 
class MockStorage(StorageInterface):

    """

    Mock-Speicher für Tests, GUI und Entwicklung.

    Arbeitet komplett in Memory und simuliert eine echte Datenbank-/Dateistruktur.

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

        """Gibt die komplette interne Datenstruktur zurück (MVP-ready)."""

        return self._data
 
    def save_data(self, data: dict) -> None:

        """Speichert Daten wie eine echte JSON-Datei."""

        if not isinstance(data, dict):

            raise ValueError("Storage error: Data must be a dictionary")

        self._data = data

 