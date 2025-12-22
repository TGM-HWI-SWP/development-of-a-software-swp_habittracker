# Diese Klasse verwaltet alle Daten und die Logik des Habit Trackers
# Sie kümmert sich NICHT um die Oberfläche, sondern nur um:
# - Habits speichern
# - XP berechnen
# - Level erhöhen
class HabitManager:

    # Feste Werte (Konstanten):
    # Wie viele XP man pro erledigtem Habit bekommt
    XP_PER_HABIT = 10

    # Wie viele XP man für einen Levelaufstieg braucht
    XP_PER_LEVEL = 100

    # Konstruktor der Klasse
    # storage ist ein Objekt, das für das Speichern und Laden der Daten zuständig ist
    def __init__(self, storage):
        self.storage = storage  # Speichert das Speicher-Objekt
        self.habits = self.storage.load_habits()  # Lädt gespeicherte Habits
        self.level = 1  # Startlevel
        self.xp = 0  # Aktuelle XP im aktuellen Level
        self.total_xp = 0  # Insgesamt gesammelte XP

    # Gibt alle Habits zurück (z. B. für die Anzeige in der GUI)
    def get_habits(self):
        return self.habits

    # Prüft, ob ein neues Habit hinzugefügt werden darf
    # Das Limit steigt mit höherem Level
    def can_add_habit(self):
        limit = 10  # Standard-Limit für Anfänger

        # Ab Level 5 darf man mehr Habits haben
        if self.level >= 5:
            limit = 12

        # Ab Level 10 noch mehr
        if self.level >= 10:
            limit = 15

        # Gibt True zurück, wenn noch Platz für ein Habit ist
        return len(self.habits) < limit

    # Fügt ein neues Habit hinzu
    def add_habit(self, name, desc, freq):
        # Erstellt ein neues Habit als Dictionary
        self.habits.append({
            "name": name,                 # Name des Habits
            "description": desc,          # Beschreibung
            "frequency": freq,            # Häufigkeit (daily, weekly, monthly)
            "is_done_today": False        # Anfangs noch nicht erledigt
        })

        # Speichert die aktualisierte Habit-Liste
        self.storage.save_habits(self.habits)

    # Aktualisiert ein bestehendes Habit
    def update_habit(self, old, new, desc, freq):
        # Durchläuft alle Habits
        for h in self.habits:
            # Sucht das Habit mit dem alten Namen
            if h["name"] == old:
                h["name"] = new
                h["description"] = desc
                h["frequency"] = freq

        # Speichert die Änderungen
        self.storage.save_habits(self.habits)

    # Löscht ein Habit anhand seines Namens
    def delete_habit(self, name):
        # Erstellt eine neue Liste ohne das zu löschende Habit
        self.habits = [h for h in self.habits if h["name"] != name]

        # Speichert die neue Liste
        self.storage.save_habits(self.habits)

    # Markiert ein Habit als erledigt oder nicht erledigt
    def set_habit_done(self, name, done):
        # Durchläuft alle Habits
        for h in self.habits:
            if h["name"] == name:

                # Falls das Habit neu als erledigt markiert wird,
                # bekommt der Nutzer XP
                if done and not h["is_done_today"]:
                    self._add_xp(self.XP_PER_HABIT)

                # Setzt den neuen Status
                h["is_done_today"] = done

        # Speichert den neuen Status
        self.storage.save_habits(self.habits)

    # Interne Methode zum Hinzufügen von XP
    # (wird nur innerhalb der Klasse verwendet)
    def _add_xp(self, amount):
        self.xp += amount          # Fügt XP für das aktuelle Level hinzu
        self.total_xp += amount    # Erhöht die Gesamt-XP

        # Prüft, ob ein Levelaufstieg erreicht wurde
        if self.xp >= self.XP_PER_LEVEL:
            self.xp -= self.XP_PER_LEVEL  # Überschüssige XP bleiben erhalten
            self.level += 1               # Level wird erhöht

    # Gibt das aktuelle Level zurück
    def get_level(self):
        return self.level

    # Gibt die insgesamt gesammelten XP zurück
    def get_total_xp(self):
        return self.total_xp

    # Gibt den Fortschritt zum nächsten Level zurück (0.0 – 1.0)
    # Wird für den Fortschrittsbalken in der GUI genutzt
    def get_xp_progress(self):
        return self.xp / self.XP_PER_LEVEL
