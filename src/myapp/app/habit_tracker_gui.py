import customtkinter as ctk
from tkinter import messagebox


class HabitTrackerGUI(ctk.CTk):
    """
    Moderne MVP-GUI für den Habit Tracker.
    """

    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.title("Habit Tracker")
        self.geometry("700x500")
        self.resizable(False, False)

        # ===== Layout =====
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_habit_list()
        self._create_footer()

        self.refresh_habits()

    # ---------------- HEADER ----------------
    def _create_header(self):
        header = ctk.CTkFrame(self, height=60)
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        title = ctk.CTkLabel(
            header,
            text="📅 Habit Tracker",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left", padx=20)

        add_button = ctk.CTkButton(
            header,
            text="➕ Neues Habit",
            command=self._open_add_habit_window
        )
        add_button.pack(side="right", padx=20)

    # ---------------- LIST ----------------
    def _create_habit_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=10)

    def refresh_habits(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        habits = self.manager.get_habits()

        if not habits:
            ctk.CTkLabel(
                self.list_frame,
                text="Noch keine Habits vorhanden 😴"
            ).pack(pady=20)
            return

        for habit in habits:
            self._create_habit_card(habit)

    def _create_habit_card(self, habit: dict):
        card = ctk.CTkFrame(self.list_frame)
        card.pack(fill="x", pady=5, padx=5)

        name_label = ctk.CTkLabel(
            card,
            text=habit["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        desc_label = ctk.CTkLabel(
            card,
            text=habit["description"],
            text_color="gray"
        )
        desc_label.grid(row=1, column=0, sticky="w", padx=10)

        status = "✅ Erledigt" if habit["is_done_today"] else "❌ Offen"

        status_label = ctk.CTkLabel(card, text=status)
        status_label.grid(row=0, column=1, padx=10)

        toggle_button = ctk.CTkButton(
            card,
            text="✔ / ✖",
            width=60,
            command=lambda: self._toggle_habit(habit["name"])
        )
        toggle_button.grid(row=0, column=2, padx=5)

        delete_button = ctk.CTkButton(
            card,
            text="🗑",
            width=40,
            fg_color="darkred",
            hover_color="red",
            command=lambda: self._delete_habit(habit["name"])
        )
        delete_button.grid(row=0, column=3, padx=5)

    # ---------------- FOOTER ----------------
    def _create_footer(self):
        footer = ctk.CTkFrame(self, height=40)
        footer.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        refresh_btn = ctk.CTkButton(
            footer,
            text="🔄 Aktualisieren",
            command=self.refresh_habits
        )
        refresh_btn.pack()

    # ---------------- ACTIONS ----------------
    def _toggle_habit(self, name: str):
        self.manager.toggle_habit(name)
        self.refresh_habits()

    def _delete_habit(self, name: str):
        if messagebox.askyesno("Löschen", f"Habit '{name}' wirklich löschen?"):
            self.manager.delete_habit(name)
            self.refresh_habits()

    def _open_add_habit_window(self):
        window = ctk.CTkToplevel(self)
        window.title("Neues Habit")
        window.geometry("400x300")
        window.grab_set()

        name_entry = ctk.CTkEntry(window, placeholder_text="Name")
        name_entry.pack(pady=10, padx=20, fill="x")

        desc_entry = ctk.CTkEntry(window, placeholder_text="Beschreibung")
        desc_entry.pack(pady=10, padx=20, fill="x")

        freq_entry = ctk.CTkEntry(window, placeholder_text="Frequenz (z.B. daily)")
        freq_entry.pack(pady=10, padx=20, fill="x")

        def save():
            self.manager.add_habit(
                name_entry.get(),
                desc_entry.get(),
                freq_entry.get()
            )
            window.destroy()
            self.refresh_habits()

        save_button = ctk.CTkButton(window, text="Speichern", command=save)
        save_button.pack(pady=20)
