import customtkinter as ctk
 
 
class HabitTrackerGUI(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
 
        self.title("Habit Tracker")
        self.geometry("860x600")
        self.resizable(False, False)
 
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
 
        self._last_xp_gain = 0
 
        self._create_header()
        self._create_list()
        self._create_xp_section()
        self._refresh()
 
    # ---------- HEADER ----------
    def _create_header(self):
        frame = ctk.CTkFrame(self, height=60, corner_radius=16)
        frame.grid(row=0, column=0, sticky="ew", padx=14, pady=14)
 
        ctk.CTkLabel(
            frame,
            text="📅 Habit Tracker",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(side="left", padx=20)
 
        ctk.CTkButton(
            frame,
            text="+ Neues Habit",
            height=36,
            corner_radius=18,
            command=self._open_add_habit
        ).pack(side="right", padx=20)
 
    # ---------- HABIT LIST ----------
    def _create_list(self):
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=18
        )
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=14)
 
    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
 
        for habit in self.manager.get_habits():
            self._habit_row(habit)
 
        self._update_xp_section()
 
    def _habit_row(self, habit):
        row = ctk.CTkFrame(
            self.list_frame,
            height=70,
            corner_radius=16
        )
        row.pack(fill="x", pady=8, padx=8)
 
        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=14)
 
        ctk.CTkLabel(
            left,
            text=habit["name"],
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(anchor="w")
 
        ctk.CTkLabel(
            left,
            text=f'{habit["description"]} • {habit["frequency"].upper()}',
            text_color="#aaaaaa"
        ).pack(anchor="w")
 
        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right", padx=14)
 
        status_color = "#2ecc71" if habit["is_done_today"] else "#e74c3c"
        status_text = "Erledigt" if habit["is_done_today"] else "Offen"
 
        ctk.CTkLabel(
            right,
            text=status_text,
            text_color=status_color,
            width=80
        ).pack(side="left", padx=6)
 
        ctk.CTkButton(
            right,
            text="✔",
            width=42,
            height=32,
            corner_radius=16,
            command=lambda: self._set_done(habit["name"], True)
        ).pack(side="left", padx=4)
 
        ctk.CTkButton(
            right,
            text="✖",
            width=42,
            height=32,
            corner_radius=16,
            fg_color="#555555",
            command=lambda: self._set_done(habit["name"], False)
        ).pack(side="left", padx=4)
 
        ctk.CTkButton(
            right,
            text="✏️",
            width=42,
            height=32,
            corner_radius=16,
            command=lambda: self._open_edit_habit(habit)
        ).pack(side="left", padx=4)
 
    # ---------- XP SECTION ----------
    def _create_xp_section(self):
        frame = ctk.CTkFrame(self, height=90, corner_radius=18)
        frame.grid(row=2, column=0, sticky="ew", padx=14, pady=14)
 
        self.level_label = ctk.CTkLabel(
            frame,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.level_label.pack(pady=(10, 2))
 
        self.xp_bar = ctk.CTkProgressBar(
            frame,
            height=18,
            corner_radius=10
        )
        self.xp_bar.pack(fill="x", padx=20)
 
        self.xp_info = ctk.CTkLabel(
            frame,
            text_color="#aaaaaa"
        )
        self.xp_info.pack(pady=(4, 8))
 
    def _update_xp_section(self):
        self.level_label.configure(
            text=f"Level {self.manager.get_level()} • Gesamt XP: {self.manager.get_total_xp()}"
        )
 
        self.xp_bar.set(self.manager.get_xp_progress())
 
        if self._last_xp_gain > 0:
            self.xp_info.configure(text=f"+{self._last_xp_gain} XP erhalten 🎉")
        else:
            self.xp_info.configure(text="")
 
        self._last_xp_gain = 0
 
    # ---------- ACTIONS ----------
    def _set_done(self, name, done):
        before_xp = self.manager.get_total_xp()
        self.manager.set_habit_done(name, done)
        after_xp = self.manager.get_total_xp()
 
        self._last_xp_gain = after_xp - before_xp
        self._refresh()
 
    def _open_add_habit(self):
        self._open_habit_editor()
 
    def _open_edit_habit(self, habit):
        self._open_habit_editor(habit)
 
    def _open_habit_editor(self, habit=None):
        win = ctk.CTkToplevel(self)
        win.title("Habit bearbeiten" if habit else "Neues Habit")
        win.geometry("420x380")
        win.grab_set()
 
        ctk.CTkLabel(win, text="Name").pack(pady=(20, 0))
        name = ctk.CTkEntry(win)
        name.pack(padx=20, fill="x")
 
        ctk.CTkLabel(win, text="Beschreibung").pack(pady=(10, 0))
        desc = ctk.CTkEntry(win)
        desc.pack(padx=20, fill="x")
 
        ctk.CTkLabel(win, text="Frequenz").pack(pady=(10, 0))
        freq = ctk.CTkOptionMenu(
            win,
            values=["daily", "weekly", "monthly"]
        )
        freq.pack()
 
        if habit:
            name.insert(0, habit["name"])
            desc.insert(0, habit["description"])
            freq.set(habit["frequency"])
 
        def save():
            if habit:
                self.manager.update_habit(
                    habit["name"],
                    name.get(),
                    desc.get(),
                    freq.get()
                )
            else:
                self.manager.add_habit(
                    name.get(),
                    desc.get(),
                    freq.get()
                )
            win.destroy()
            self._refresh()
 
        ctk.CTkButton(
            win,
            text="Speichern",
            height=36,
            corner_radius=18,
            command=save
        ).pack(pady=24)