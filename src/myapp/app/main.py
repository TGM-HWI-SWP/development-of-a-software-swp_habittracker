from myapp.dummies.mock_storage import MockStorage
from myapp.models.habit_model import HabitModel
from myapp.controllers.habit_controller import HabitController
 
def main():
    # Mock-Datenbank statt JSON-Datei
    storage = MockStorage()
 
    # Model + Controller initialisieren
    model = HabitModel(storage)
    controller = HabitController(model)
 
    # --- MVP TESTAUSGABE ---
    print("==== HABIT TRACKER MVP ====")
    habits = controller.list_habits()
    for h in habits:
        status = "✅" if h["is_done_today"] else "❌"
        print(f"{h['name']} ({h['frequency']}) - {status}")
 
    print("\nMarkiere 'Wasser trinken' als erledigt...")
    controller.finish_habit("Wasser trinken")
 
    print("\nNeuer Status:")
    habits = controller.list_habits()
    for h in habits:
        status = "✅" if h["is_done_today"] else "❌"
        print(f"{h['name']} ({h['frequency']}) - {status}")
 
if __name__ == "__main__":
    main()