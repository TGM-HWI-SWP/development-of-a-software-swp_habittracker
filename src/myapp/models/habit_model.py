class HabitModel:
    def __init__(self, storage):
        self.storage = storage
        self.data = self.storage.load_data()
 
    def get_habits(self):
        return self.data.get("habits", [])
 
    def mark_done(self, habit_name: str):
        for habit in self.data["habits"]:
            if habit["name"] == habit_name:
                habit["is_done_today"] = True
                self.storage.save_data(self.data)
                return True
        return False