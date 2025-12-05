"""
Main entry point for the Habit Tracker application.
Initializes storage, business logic, XP system, and the GUI.
"""

from myapp.adapters.json_storage import JSONStorage
from myapp.business_logic.habit_manager import HabitManager
from myapp.business_logic.xp_system import XPSystem
from myapp.app.habit_tracker_gui import HabitTrackerGUI

import customtkinter as ctk

# Test Comment!


def main() -> None:
    """
    Startet die Habit-Tracker-Applikation mit
    Storage, Manager, XP-System und GUI.
    """
    # Storages und Systeme initialisieren
    storage = JSONStorage()
    xp_system = XPSystem()

    # Manager für die Geschäftslogik laden
    manager = HabitManager(storage=storage, xp_system=xp_system)

    # CustomTkinter konfigurieren
    ctk.set_appearance_mode("dark")        # dark/light/system
    ctk.set_default_color_theme("blue")    # blue/green/dark-blue

    # GUI starten
    app = HabitTrackerGUI(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
