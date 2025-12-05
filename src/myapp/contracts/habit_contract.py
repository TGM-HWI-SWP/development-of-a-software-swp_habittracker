class HabitContract:
    """
    Vertrag eines Habits.
    Enthält nur Datenstruktur, KEINE Logik.
    """

    def __init__(self, name: str, description: str, frequency: str, is_done_today: bool = False):
        self.name = name
        self.description = description
        self.frequency = frequency
        self.is_done_today = is_done_today

    def to_dict(self) -> dict:
        """Nur Struktur, keine Logik."""
        return {
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "is_done_today": self.is_done_today
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Statische Fabrik – nur Daten übernehmen.
        Keine Logik.
        """
        return HabitContract(
            name=data.get("name", ""),
            description=data.get("description", ""),
            frequency=data.get("frequency", ""),
            is_done_today=data.get("is_done_today", False)
        )
