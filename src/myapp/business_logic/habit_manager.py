class HabitManager:
    XP_PER_HABIT = 10
    XP_PER_LEVEL = 100

    def __init__(self, storage):
        self.storage = storage
        self.habits = self.storage.load_habits()
        self.level = 1
        self.xp = 0
        self.total_xp = 0

    def get_habits(self):
        return self.habits

    def can_add_habit(self):
        limit = 10
        if self.level >= 5:
            limit = 12
        if self.level >= 10:
            limit = 15
        return len(self.habits) < limit

    def add_habit(self, name, desc, freq):
        self.habits.append({
            "name": name,
            "description": desc,
            "frequency": freq,
            "is_done_today": False
        })
        self.storage.save_habits(self.habits)

    def update_habit(self, old, new, desc, freq):
        for h in self.habits:
            if h["name"] == old:
                h["name"] = new
                h["description"] = desc
                h["frequency"] = freq
        self.storage.save_habits(self.habits)

    def delete_habit(self, name):
        self.habits = [h for h in self.habits if h["name"] != name]
        self.storage.save_habits(self.habits)

    def set_habit_done(self, name, done):
        for h in self.habits:
            if h["name"] == name:
                if done and not h["is_done_today"]:
                    self._add_xp(self.XP_PER_HABIT)
                h["is_done_today"] = done
        self.storage.save_habits(self.habits)

    def _add_xp(self, amount):
        self.xp += amount
        self.total_xp += amount
        if self.xp >= self.XP_PER_LEVEL:
            self.xp -= self.XP_PER_LEVEL
            self.level += 1

    def get_level(self):
        return self.level

    def get_total_xp(self):
        return self.total_xp

    def get_xp_progress(self):
        return self.xp / self.XP_PER_LEVEL
