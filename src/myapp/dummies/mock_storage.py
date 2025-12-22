class MockStorage:
    def __init__(self):
        self.habits = [
            {"name": "Wasser trinken", "description": "2 Liter", "frequency": "daily", "is_done_today": False},
            {"name": "Spazieren", "description": "30 Minuten", "frequency": "daily", "is_done_today": True},
        ]

    def load_habits(self):
        return self.habits

    def save_habits(self, habits):
        self.habits = habits
