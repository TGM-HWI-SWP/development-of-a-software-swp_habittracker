class HabitContract:
    """
    Datenvertrag für ein Habit.
    KEINE Logik, nur Struktur.
    """

    def __init__(
        self,
        name: str,
        description: str,
        frequency: str,
        is_done_today: bool = False
    ):
        self.name = name
        self.description = description
        self.frequency = frequency
        self.is_done_today = is_done_today

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "is_done_today": self.is_done_today
        }