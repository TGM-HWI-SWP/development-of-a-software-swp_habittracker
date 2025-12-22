import customtkinter as ctk


class HabitTrackerGUI(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.editing_name = None

        self.title("Habit Tracker")
        self.geometry("920x650")
        self.resizable(False, False)

        self._create_header()
        self._create_form()
        self._create_list()
        self._create_xp()

        self.refresh()

    # ---------- HEADER ----------
    def _create_header(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=15)

        self.title_lbl = ctk.CTkLabel(
            frame,
            text="Habit Tracker",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_lbl.pack(side="left")

    # ---------- FORM ----------
    def _create_form(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=10)

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Name")
        self.name_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.desc_entry = ctk.CTkEntry(frame, placeholder_text="Beschreibung")
        self.desc_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.freq_menu = ctk.CTkOptionMenu(
            frame,
            values=["daily", "weekly", "monthly"]
        )
        self.freq_menu.pack(side="left", padx=5)

        self.submit_btn = ctk.CTkButton(
            frame,
            text="Hinzufügen",
            command=self.submit_habit
        )
        self.submit_btn.pack(side="left", padx=5)

        self.error_lbl = ctk.CTkLabel(frame, text="", text_color="#ff6b6b")
        self.error_lbl.pack(side="left", padx=10)

    # ---------- LIST ----------
    def _create_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(fill="both", expand=True, padx=20)

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for h in self.manager.get_habits():
            self._habit_row(h)

        self._update_xp()

    def _habit_row(self, h):
        row = ctk.CTkFrame(self.list_frame)
        row.pack(fill="x", pady=6)

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkLabel(
            left,
            text=h["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text=f'{h["description"]} • {h["frequency"]}',
            text_color="#aaaaaa"
        ).pack(anchor="w")

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right", padx=10)

        status = "Erledigt" if h["is_done_today"] else "Offen"
        color = "#2ecc71" if h["is_done_today"] else "#e74c3c"

        ctk.CTkLabel(right, text=status, text_color=color).pack(side="left", padx=6)

        ctk.CTkButton(right, text="✔", width=40,
                      command=lambda: self.set_done(h["name"], True)).pack(side="left", padx=2)

        ctk.CTkButton(right, text="✖", width=40,
                      command=lambda: self.set_done(h["name"], False)).pack(side="left", padx=2)

        ctk.CTkButton(right, text="✏", width=40,
                      command=lambda: self.start_edit(h)).pack(side="left", padx=2)

        ctk.CTkButton(right, text="🗑", width=40,
                      command=lambda: self.delete_habit(h["name"])).pack(side="left", padx=2)

    # ---------- XP ----------
    def _create_xp(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=15)

        self.xp_lbl = ctk.CTkLabel(frame)
        self.xp_lbl.pack()

        self.xp_bar = ctk.CTkProgressBar(frame)
        self.xp_bar.pack(fill="x", padx=20, pady=5)

    def _update_xp(self):
        self.xp_lbl.configure(
            text=f"Level {self.manager.get_level()} • {self.manager.get_total_xp()} XP"
        )
        self.xp_bar.set(self.manager.get_xp_progress())

    # ---------- ACTIONS ----------
    def submit_habit(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        freq = self.freq_menu.get()

        if self.editing_name:
            error = self.manager.update_habit(self.editing_name, name, desc, freq)
        else:
            error = self.manager.add_habit(name, desc, freq)

        if error:
            self.error_lbl.configure(text=error)
            return

        self.clear_form()
        self.refresh()

    def start_edit(self, habit):
        self.editing_name = habit["name"]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, habit["name"])
        self.desc_entry.delete(0, "end")
        self.desc_entry.insert(0, habit["description"])
        self.freq_menu.set(habit["frequency"])
        self.submit_btn.configure(text="Speichern")

    def clear_form(self):
        self.editing_name = None
        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.submit_btn.configure(text="Hinzufügen")
        self.error_lbl.configure(text="")

    def set_done(self, name, done):
        self.manager.set_done(name, done)
        self.refresh()

    def delete_habit(self, name):
        self.manager.delete_habit(name)
        self.refresh()
