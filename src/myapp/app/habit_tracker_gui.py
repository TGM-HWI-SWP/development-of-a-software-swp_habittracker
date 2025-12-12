import customtkinter as ctk  #CustomTkinter für Tkinter-Widgets
from typing import Callable, List  #aktuell nicht genutzt, kann entfernt werden

class HabitTrackerGUI(ctk.CTk):
    #Haupt-GUI-Klasse, erbt von CTk (CustomTkinter Hauptfenster)
    def __init__(self, manager):
        super().__init__()
        self.title("Habit Tracker")      #Fenstertitel
        self.geometry("600x500")         #Fenstergröße
        self.manager = manager           #Business-Logic Manager (also HabitManager)

        #Textfeld zur Anzeige aller Habits
        self.habit_listbox = ctk.CTkTextbox(self, width=400, height=300)
        self.habit_listbox.pack(pady=20)

        #Buttons für Aktionen
        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        self.refresh_button.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Add Habit", command=self.open_add_window)
        self.add_button.pack(pady=5)

        self.mark_button = ctk.CTkButton(self, text="Mark Done", command=self.mark_done)
        self.mark_button.pack(pady=5)

        #Am Anfang die Liste füllen
        self.refresh()

    def refresh(self):
        #Inhalte werden gelöscht und alle Habits vom Manager neu einfügen
        self.habit_listbox.delete("0.0", "end")
        for habit in self.manager.get_all():
            #Erwartet, dass jedes Habit ein Objekt mit id, name und is_done_today hat
            line = f"ID {habit.id} | {habit.name} | Done today: {habit.is_done_today}\n"
            self.habit_listbox.insert("end", line)

    def open_add_window(self):
        #Pop-up zum Hinzufügen eines neuen Habits
        win = ctk.CTkToplevel(self)
        win.title("Add Habit")

        name_entry = ctk.CTkEntry(win, placeholder_text="Name")
        name_entry.pack(pady=10)

        desc_entry = ctk.CTkEntry(win, placeholder_text="Description")
        desc_entry.pack(pady=10)

        freq_entry = ctk.CTkEntry(win, placeholder_text="Frequency (daily/weekly)")
        freq_entry.pack(pady=10)

        def save():
            #Werte aus den Eingabefeldern lesen und an den Manager weitergeben
            name = name_entry.get()
            desc = desc_entry.get()
            freq = freq_entry.get() or "daily"  #Standard auf "daily" also täglich, falls nichts eingegeben ist 
            self.manager.add_habit(name, desc, freq)
            self.refresh()   #Liste aktualisieren
            win.destroy()    #Fenster schließen

        save_button = ctk.CTkButton(win, text="Save", command=save)
        save_button.pack(pady=10)

    def mark_done(self):
        #Pop-up, um ein Habit als erledigt zu markieren (per ID)
        win = ctk.CTkToplevel(self)
        win.title("Mark Habit Done")

        id_entry = ctk.CTkEntry(win, placeholder_text="Habit ID")
        id_entry.pack(pady=10)

        def submit():
            try:
                habit_id = int(id_entry.get())  #ID wird in ein int umwandeln
                self.manager.mark_done(habit_id) #Manager-Funktion wird aufgerufen
                self.refresh()                  #Liste aktualisieren
                win.destroy()                   #Fenster schließen
            except ValueError:
                # Ungültige Eingabe (kein Integer) -> aktuell ignorieren
                pass

        mark_button = ctk.CTkButton(win, text="Mark Done", command=submit)
        mark_button.pack(pady=10)




# nur mal ein Beispiel wie es ausschauen könnte
# from myapp.business_logic.habit_manager import HabitManager
# from myapp.business_logic.xp_system import XPSystem
# from myapp.adapters.json_storage import JSONStorage
#
# if __name__ == "__main__":
#     ctk.set_appearance_mode("dark")
#     storage = JSONStorage()
#     xp = XPSystem()
#     manager = HabitManager(storage, xp)
#     app = HabitTrackerGUI(manager)
#     app.mainloop()

