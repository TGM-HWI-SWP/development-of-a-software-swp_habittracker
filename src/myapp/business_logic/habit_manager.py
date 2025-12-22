class HabitManager:
    XP_PER_HABIT = 10
    XP_PER_LEVEL = 100

 

    def __init__(self, storage):
        self.storage = storage
        self.habits = storage.load_habits()
        self.level = 1
        self.xp = 0
        self.total_xp = 0

 

    # ---------- LIMIT ----------
    def max_habits(self):
        if self.level >= 10:
            return 15
        if self.level >= 5:
            return 12
        return 10

 

    # ---------- HABITS ----------
    def get_habits(self):
        return self.habits

 

    def add_habit(self, name, description, frequency, category):
        if name.strip() == "":
            return "Name darf nicht leer sein"

 

        if len(self.habits) >= self.max_habits():
            return f"Maximal {self.max_habits()} Habits erlaubt"

 

        self.habits.append({
            "name": name,
            "description": description,
            "frequency": frequency,
            "category": category,
            "streak": 0,
            "is_done_today": False
        })
        self.storage.save_habits(self.habits)
        return None

 

    def update_habit(self, old_name, new_name, description, frequency, category):
        if new_name.strip() == "":
            return "Name darf nicht leer sein"

 

        for h in self.habits:
            if h["name"] == old_name:
                h["name"] = new_name
                h["description"] = description
                h["frequency"] = frequency
                h["category"] = category

 

        self.storage.save_habits(self.habits)
        return None

 

    def delete_habit(self, name):
        self.habits = [h for h in self.habits if h["name"] != name]
        self.storage.save_habits(self.habits)

 

    def set_done(self, name, done):
        for h in self.habits:
            if h["name"] == name:
                if done and not h["is_done_today"]:
                    h["streak"] += 1
                    self._add_xp(self.XP_PER_HABIT)
                if not done:
                    h["streak"] = 0
                h["is_done_today"] = done
        self.storage.save_habits(self.habits)

 

    # ---------- XP ----------
    def _add_xp(self, amount):
        self.xp += amount
        self.total_xp += amount

 

        if self.xp >= self.XP_PER_LEVEL:
            self.xp = 0
            self.level += 1

 

    def get_level(self):
        return self.level

 

    def get_total_xp(self):
        return self.total_xp

 

    def get_xp_progress(self):
        return self.xp / self.XP_PER_LEVEL

import customtkinter as ctk

 

CATEGORY_COLORS = {
    "Sehr wichtig": "#e74c3c",
    "Wichtig": "#f39c12",
    "Normal": "#3498db",
    "Unwichtig": "#7f8c8d"
}