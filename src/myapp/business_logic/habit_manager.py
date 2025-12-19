class HabitManager:
    """
    Zentrale Geschäftslogik für Habits + XP-System.
    """

    XP_PER_HABIT = 10
    XP_PER_LEVEL = 100

    def __init__(self, storage):
        self._storage = storage
        self._habits = self._storage.load_habits()

        self._level = 1
        self._xp = 0
        self._total_xp = 0

    # ---------- HABITS ----------
    def get_habits(self):
        return self._habits

    def add_habit(self, name: str, description: str, frequency: str):
        self._habits.append({
            "name": name,
            "description": description,
            "frequency": frequency,
            "is_done_today": False
        })
        self._storage.save_habits(self._habits)

    def delete_habit(self, name: str):
        self._habits = [h for h in self._habits if h["name"] != name]
        self._storage.save_habits(self._habits)

    def update_habit(self, old_name: str, new_name: str, description: str, frequency: str):
        for habit in self._habits:
            if habit["name"] == old_name:
                habit["name"] = new_name
                habit["description"] = description
                habit["frequency"] = frequency
        self._storage.save_habits(self._habits)

    def set_habit_done(self, name: str, done: bool):
        for habit in self._habits:
            if habit["name"] == name:
                if done and not habit["is_done_today"]:
                    self._add_xp(self.XP_PER_HABIT)
                habit["is_done_today"] = done
        self._storage.save_habits(self._habits)

    # ---------- XP / LEVEL ----------
    def _add_xp(self, amount: int):
        self._xp += amount
        self._total_xp += amount

        if self._xp >= self.XP_PER_LEVEL:
            self._xp -= self.XP_PER_LEVEL
            self._level += 1

    def get_level(self) -> int:
        return self._level

    def get_xp(self) -> int:
        return self._xp

    def get_total_xp(self) -> int:
        return self._total_xp

    def get_xp_progress(self) -> float:
        return self._xp / self.XP_PER_LEVEL
