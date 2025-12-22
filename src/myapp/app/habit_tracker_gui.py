# Importiert die Bibliothek "customtkinter"
# Diese ist eine modernere Version von tkinter und wird für grafische Benutzeroberflächen genutzt
import customtkinter as ctk


# Definition einer Klasse für die grafische Oberfläche des Habit Trackers
# Die Klasse erbt von CTk, also dem Hauptfenster von customtkinter
class HabitTrackerGUI(ctk.CTk):

    # Konstruktor der Klasse
    # Er wird automatisch aufgerufen, wenn ein Objekt dieser Klasse erstellt wird
    # manager ist ein Objekt, das sich um die Daten (Habits, XP, Level etc.) kümmert
    def _init_(self, manager):
        super()._init_()  # Ruft den Konstruktor der Elternklasse (CTk) auf
        self.manager = manager  # Speichert den Manager für späteren Zugriff
        self.editing_name = None  # Merkt sich, ob gerade ein Habit bearbeitet wird

        # Setzt den Fenstertitel
        self.title("Habit Tracker")

        # Setzt die Fenstergröße (Breite x Höhe)
        self.geometry("960x720")

        # Verhindert, dass das Fenster in der Größe verändert werden kann
        self.resizable(False, False)

        # Konfiguriert das Grid-Layout (Spalten und Zeilen)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Erstellt die einzelnen Bereiche der Oberfläche
        self._create_header()
        self._create_form()
        self._create_list()
        self._create_xp()

        # Aktualisiert die Anzeige (z. B. Liste der Habits)
        self.refresh()

    # ---------- HEADER ----------
    # Erstellt den oberen Bereich mit der Überschrift
    def _create_header(self):
        # Erstellt einen Rahmen (Frame) für den Header
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=0, column=0, padx=14, pady=14, sticky="ew")

        # Erstellt eine Textbeschriftung mit Emoji und Titel
        ctk.CTkLabel(
            frame,
            text="📅 Habit Tracker",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(padx=20, pady=12)

    # ---------- FORM ----------
    # Erstellt das Formular zum Hinzufügen oder Bearbeiten von Habits
    def _create_form(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=1, column=0, padx=14, pady=(0, 10), sticky="ew")

        # Eingabefeld für den Namen des Habits
        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Habit Name")
        self.name_entry.pack(side="left", padx=8, pady=10, fill="x", expand=True)

        # Wenn die Enter-Taste gedrückt wird, wird das Habit gespeichert
        self.name_entry.bind("<Return>", lambda e: self.save_habit())

        # Eingabefeld für die Beschreibung des Habits
        self.desc_entry = ctk.CTkEntry(frame, placeholder_text="Beschreibung")
        self.desc_entry.pack(side="left", padx=8, pady=10, fill="x", expand=True)

        # Dropdown-Menü zur Auswahl der Häufigkeit
        self.freq_menu = ctk.CTkOptionMenu(frame, values=["daily", "weekly", "monthly"])
        self.freq_menu.pack(side="left", padx=8)

        # Button zum Hinzufügen oder Speichern eines Habits
        self.save_btn = ctk.CTkButton(
            frame,
            text="Hinzufügen",
            width=120,
            command=self.save_habit
        )
        self.save_btn.pack(side="right", padx=8)

        # Label für Fehlermeldungen (z. B. leerer Name)
        self.error_label = ctk.CTkLabel(frame, text="", text_color="#e74c3c")
        self.error_label.pack(side="right", padx=8)

    # ---------- LIST ----------
    # Erstellt den scrollbaren Bereich für die Habit-Liste
    def _create_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=16)
        self.list_frame.grid(row=2, column=0, padx=16, pady=12, sticky="nsew")

    # Aktualisiert die komplette Anzeige
    def refresh(self):
        # Entfernt alle bisherigen Habit-Einträge
        for w in self.list_frame.winfo_children():
            w.destroy()

        # Fügt alle Habits aus dem Manager neu hinzu
        for h in self.manager.get_habits():
            self._habit_row(h)

        # Aktualisiert XP und Level
        self._update_xp()

    # Erstellt eine einzelne Zeile für ein Habit
    def _habit_row(self, h):
        row = ctk.CTkFrame(self.list_frame, corner_radius=14)
        row.pack(fill="x", pady=6, padx=6)

        # Linker Bereich für Textinformationen
        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=10)

        # Anzeigename des Habits
        ctk.CTkLabel(
            left,
            text=h["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        # Beschreibung und Frequenz
        ctk.CTkLabel(
            left,
            text=f'{h["description"]} • {h["frequency"]}',
            text_color="#aaaaaa"
        ).pack(anchor="w")

        # Status: erledigt oder offen
        status_text = "Erledigt" if h["is_done_today"] else "Offen"
        status_color = "#2ecc71" if h["is_done_today"] else "#e74c3c"

        # Anzeige des Status
        ctk.CTkLabel(
            left,
            text=status_text,
            text_color=status_color,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(2, 0))

        # Rechter Bereich mit Aktionsbuttons
        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right", padx=10)

        # Button: Habit als erledigt markieren
        ctk.CTkButton(
            right, text="✔", width=36,
            command=lambda: self.toggle(h["name"], True)
        ).pack(side="left", padx=2)

        # Button: Habit als nicht erledigt markieren
        ctk.CTkButton(
            right, text="✖", width=36,
            command=lambda: self.toggle(h["name"], False)
        ).pack(side="left", padx=2)

        # Button: Habit bearbeiten
        ctk.CTkButton(
            right, text="✏", width=36,
            command=lambda: self.start_edit(h)
        ).pack(side="left", padx=2)

        # Button: Habit löschen
        ctk.CTkButton(
            right, text="🗑", width=36,
            command=lambda: self.delete(h["name"])
        ).pack(side="left", padx=2)

    # ---------- ACTIONS ----------
    # Speichert ein neues Habit oder aktualisiert ein bestehendes
    def save_habit(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        freq = self.freq_menu.get()

        # Überprüfung: Name darf nicht leer sein
        if name == "":
            self.error_label.configure(text="Name darf nicht leer sein")
            return

        # Neues Habit hinzufügen
        if not self.editing_name:
            if not self.manager.can_add_habit():
                self.error_label.configure(text="Habit-Limit erreicht")
                return
            self.manager.add_habit(name, desc, freq)
        else:
            # Vorhandenes Habit bearbeiten
            self.manager.update_habit(self.editing_name, name, desc, freq)
            self.editing_name = None
            self.save_btn.configure(text="Hinzufügen")

        # Eingabefelder zurücksetzen
        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.error_label.configure(text="")
        self.refresh()

    # Startet den Bearbeitungsmodus für ein Habit
    def start_edit(self, habit):
        self.editing_name = habit["name"]

        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")

        self.name_entry.insert(0, habit["name"])
        self.desc_entry.insert(0, habit["description"])
        self.freq_menu.set(habit["frequency"])

        self.save_btn.configure(text="Speichern")

    # Setzt den Status eines Habits (erledigt / nicht erledigt)
    def toggle(self, name, done):
        self.manager.set_habit_done(name, done)
        self.refresh()

    # Löscht ein Habit
    def delete(self, name):
        self.manager.delete_habit(name)
        self.refresh()

    # ---------- XP ----------
    # Erstellt den Bereich für XP und Level
    def _create_xp(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=3, column=0, padx=14, pady=14, sticky="ew")

        # Label für Level und XP
        self.xp_label = ctk.CTkLabel(frame)
        self.xp_label.pack(pady=(10, 4))

        # Fortschrittsbalken für XP
        self.xp_bar = ctk.CTkProgressBar(frame, height=16)
        self.xp_bar.pack(fill="x", padx=20, pady=(0, 10))

    # Aktualisiert die XP-Anzeige
    def _update_xp(self):
        self.xp_label.configure(
            text=f"Level {self.manager.get_level()} • {self.manager.get_total_xp()} XP"
        )
        self.xp_bar.set(self.manager.get_xp_progress())
