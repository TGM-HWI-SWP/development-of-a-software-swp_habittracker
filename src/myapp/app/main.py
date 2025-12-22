import customtkinter as ctk
from myapp.business_logic.habit_manager import HabitManager
from myapp.dummies.mock_storage import MockStorage
from myapp.app.habit_tracker_gui import HabitTrackerGUI


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    manager = HabitManager(MockStorage())
    app = HabitTrackerGUI(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
