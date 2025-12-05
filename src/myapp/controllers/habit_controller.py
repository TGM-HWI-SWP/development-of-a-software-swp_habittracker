class HabitController:
    def __init__(self, model):
        self.model = model
 
    def list_habits(self):
        return self.model.get_habits()
 
    def finish_habit(self, name):
        return self.model.mark_done(name)