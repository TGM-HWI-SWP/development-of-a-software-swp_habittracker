import customtkinter as ctk


class HabitTrackerGUI(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.editing_name = None

        self.title("Habit Tracker")
        self.geometry("960x720")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._create_header()
        self._create_form()
        self._create_list()
        self._create_xp()

        self.refresh()

    # ---------- HEADER ----------
    def _create_header(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=0, column=0, padx=14, pady=14, sticky="ew")

        ctk.CTkLabel(
            frame,
            text="📅 Habit Tracker",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(padx=20, pady=12)

    # ---------- FORM ----------
    def _create_form(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=1, column=0, padx=14, pady=(0, 10), sticky="ew")

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Habit Name")
        self.name_entry.pack(side="left", padx=8, pady=10, fill="x", expand=True)
        self.name_entry.bind("<Return>", lambda e: self.save_habit())

        self.desc_entry = ctk.CTkEntry(frame, placeholder_text="Beschreibung")
        self.desc_entry.pack(side="left", padx=8, pady=10, fill="x", expand=True)

        self.freq_menu = ctk.CTkOptionMenu(frame, values=["daily", "weekly", "monthly"])
        self.freq_menu.pack(side="left", padx=8)

        self.save_btn = ctk.CTkButton(
            frame,
            text="Hinzufügen",
            width=120,
            command=self.save_habit
        )
        self.save_btn.pack(side="right", padx=8)

        self.error_label = ctk.CTkLabel(frame, text="", text_color="#e74c3c")
        self.error_label.pack(side="right", padx=8)

    # ---------- LIST ----------
    def _create_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self, corner_radius=16)
        self.list_frame.grid(row=2, column=0, padx=16, pady=12, sticky="nsew")

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for h in self.manager.get_habits():
            self._habit_row(h)

        self._update_xp()

    def _habit_row(self, h):
        row = ctk.CTkFrame(self.list_frame, corner_radius=14)
        row.pack(fill="x", pady=6, padx=6)

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=10)

        # Name
        ctk.CTkLabel(
            left,
            text=h["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        # Beschreibung + Frequenz
        ctk.CTkLabel(
            left,
            text=f'{h["description"]} • {h["frequency"]}',
            text_color="#aaaaaa"
        ).pack(anchor="w")

        # STATUS (NEU)
        status_text = "Erledigt" if h["is_done_today"] else "Offen"
        status_color = "#2ecc71" if h["is_done_today"] else "#e74c3c"

        ctk.CTkLabel(
            left,
            text=status_text,
            text_color=status_color,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right", padx=10)

        ctk.CTkButton(
            right, text="✔", width=36,
            command=lambda: self.toggle(h["name"], True)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            right, text="✖", width=36,
            command=lambda: self.toggle(h["name"], False)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            right, text="✏", width=36,
            command=lambda: self.start_edit(h)
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            right, text="🗑", width=36,
            command=lambda: self.delete(h["name"])
        ).pack(side="left", padx=2)


    # ---------- ACTIONS ----------
    def save_habit(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        freq = self.freq_menu.get()

        if name == "":
            self.error_label.configure(text="Name darf nicht leer sein")
            return

        if not self.editing_name:
            if not self.manager.can_add_habit():
                self.error_label.configure(text="Habit-Limit erreicht")
                return
            self.manager.add_habit(name, desc, freq)
        else:
            self.manager.update_habit(self.editing_name, name, desc, freq)
            self.editing_name = None
            self.save_btn.configure(text="Hinzufügen")

        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.error_label.configure(text="")
        self.refresh()

    def start_edit(self, habit):
        self.editing_name = habit["name"]
        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")

        self.name_entry.insert(0, habit["name"])
        self.desc_entry.insert(0, habit["description"])
        self.freq_menu.set(habit["frequency"])

        self.save_btn.configure(text="Speichern")

    def toggle(self, name, done):
        self.manager.set_habit_done(name, done)
        self.refresh()

    def delete(self, name):
        self.manager.delete_habit(name)
        self.refresh()

    # ---------- XP ----------
    def _create_xp(self):
        frame = ctk.CTkFrame(self, corner_radius=16)
        frame.grid(row=3, column=0, padx=14, pady=14, sticky="ew")

        self.xp_label = ctk.CTkLabel(frame)
        self.xp_label.pack(pady=(10, 4))

        self.xp_bar = ctk.CTkProgressBar(frame, height=16)
        self.xp_bar.pack(fill="x", padx=20, pady=(0, 10))

    def _update_xp(self):
        self.xp_label.configure(
            text=f"Level {self.manager.get_level()} • {self.manager.get_total_xp()} XP"
        )
        self.xp_bar.set(self.manager.get_xp_progress())
