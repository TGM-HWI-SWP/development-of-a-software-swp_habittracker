# Diese Klasse ist ein Datenmodell für die Habits
# Sie kümmert sich ausschließlich um das Laden, Verwalten
# und Speichern der Habit-Daten
class HabitModel:

    # Konstruktor der Klasse
    # storage ist ein Objekt, das für das Speichern und Laden
    # der Daten (z. B. aus einer Datei) verantwortlich ist
    def __init__(self, storage):
        self.storage = storage  # Speichert das Speicher-Objekt
        self.data = self.storage.load_data()  # Lädt alle gespeicherten Daten

    # Gibt alle gespeicherten Habits zurück
    def get_habits(self):
        # Holt die Liste "habits" aus den Daten
        # Falls sie nicht existiert, wird eine leere Liste zurückgegeben
        return self.data.get("habits", [])

    # Markiert ein bestimmtes Habit als erledigt
    def mark_done(self, habit_name: str):
        # Durchläuft alle gespeicherten Habits
        for habit in self.data["habits"]:

            # Prüft, ob der Name des Habits übereinstimmt
            if habit["name"] == habit_name:

                # Setzt den Status auf "erledigt"
                habit["is_done_today"] = True

                # Speichert die geänderten Daten dauerhaft
                self.storage.save_data(self.data)

                # Gibt True zurück, um zu zeigen, dass es funktioniert hat
                return True

        # Falls kein Habit mit diesem Namen gefunden wurde,
        # wird False zurückgegeben
        return False
