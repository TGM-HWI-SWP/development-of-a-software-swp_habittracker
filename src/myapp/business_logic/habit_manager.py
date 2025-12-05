from contracts.habit_contract import HabitContract
from myapp.contracts.storage_interface import StorageInterface

class HabitManager:
    """
    Verantwortlich für:
    - Habits laden
    - Habits speichern
    - Logik ausführen (abhaken, neu anlegen etc.)
    """

    def __init__(self, storage: StorageInterface):
        self.storage = storage
        self.habits = self._load()

    def _load(self):
        data = self.storage.load_data()
        return [HabitContract.from_dict(h) for h in data.get("habits", [])]

    def save(self):
        data = {"habits": [h.to_dict() for h in self.habits]}
        self.storage.save_data(data)

    def add_habit(self, name, description, frequency):
        new_habit = HabitContract(name, description, frequency)
        self.habits.append(new_habit)
        self.save()

    def mark_done(self, habit_name: str):
        for h in self.habits:
            if h.name == habit_name:
                h.is_done_today = True
        self.save()
