from typing import List, Dict
from myapp.contracts.storage_interface import IStorage


class HabitManager:
    """
    Zentrale Geschäftslogik für Habits.
    """

    def __init__(self, storage: IStorage):
        self._storage = storage
        self._habits = self._storage.load_habits()

    def get_habits(self) -> List[Dict]:
        return self._habits

    def add_habit(self, name: str, description: str, frequency: str) -> None:
        self._habits.append({
            "name": name,
            "description": description,
            "frequency": frequency,
            "is_done_today": False
        })
        self._storage.save_habits(self._habits)

    def mark_done(self, name: str) -> None:
        for habit in self._habits:
            if habit["name"] == name:
                habit["is_done_today"] = True
        self._storage.save_habits(self._habits)
        
    def toggle_habit(self, name: str) -> None:
        for habit in self._habits:
            if habit["name"] == name:
                habit["is_done_today"] = not habit["is_done_today"]
        self._storage.save_habits(self._habits)

    def delete_habit(self, name: str) -> None:
        self._habits = [
            habit for habit in self._habits if habit["name"] != name
        ]
        self._storage.save_habits(self._habits)
