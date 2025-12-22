class HabitTrackerGUI(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.editing_name = None

 

        self.title("Habit Tracker")
        self.geometry("960x680")
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

 

        ctk.CTkLabel(
            frame,
            text="Habit Tracker",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(side="left")

 

    # ---------- FORM ----------
    def _create_form(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=10)

 

        self.name_entry = ctk.CTkEntry(frame, placeholder_text="Name")
        self.name_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.name_entry.bind("<Return>", lambda e: self.submit())

 

        self.desc_entry = ctk.CTkEntry(frame, placeholder_text="Beschreibung")
        self.desc_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.desc_entry.bind("<Return>", lambda e: self.submit())

 

        self.freq_menu = ctk.CTkOptionMenu(frame, values=["daily", "weekly", "monthly"])
        self.freq_menu.pack(side="left", padx=5)

 

        self.cat_menu = ctk.CTkOptionMenu(
            frame,
            values=list(CATEGORY_COLORS.keys())
        )
        self.cat_menu.pack(side="left", padx=5)
        self.cat_menu.set("Normal")

 

        self.submit_btn = ctk.CTkButton(frame, text="Hinzufügen", command=self.submit)
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

 

        color = CATEGORY_COLORS.get(h["category"], "#555")

 

        stripe = ctk.CTkFrame(row, width=6, fg_color=color)
        stripe.pack(side="left", fill="y")

 

        body = ctk.CTkFrame(row, fg_color="transparent")
        body.pack(side="left", fill="x", expand=True, padx=10)

 

        ctk.CTkLabel(body, text=h["name"],
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")

 

        ctk.CTkLabel(
            body,
            text=f'{h["description"]} • {h["frequency"]} • 🔥 {h["streak"]}',
            text_color="#aaaaaa"
        ).pack(anchor="w")

 

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right", padx=10)

 

        ctk.CTkButton(right, text="✔", width=40,
                      command=lambda: self.set_done(h["name"], True)).pack(side="left", padx=2)

 

        ctk.CTkButton(right, text="✖", width=40,
                      command=lambda: self.set_done(h["name"], False)).pack(side="left", padx=2)

 

        ctk.CTkButton(right, text="✏", width=40,
                      command=lambda: self.start_edit(h)).pack(side="left", padx=2)

 

        ctk.CTkButton(right, text="🗑", width=40,
                      command=lambda: self.delete(h["name"])).pack(side="left", padx=2)

 

    # ---------- XP ----------
    def _create_xp(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=15)

 

        self.xp_lbl = ctk.CTkLabel(frame)
        self.xp_lbl.pack()

 

        self.xp_bar = ctk.CTkProgressBar(frame)
        self.xp_bar.pack(fill="x", padx=20)

 

    def _update_xp(self):
        self.xp_lbl.configure(
            text=f"Level {self.manager.get_level()} • {self.manager.get_total_xp()} XP"
        )
        self.xp_bar.set(self.manager.get_xp_progress())

 

    # ---------- ACTIONS ----------
    def submit(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        freq = self.freq_menu.get()
        cat = self.cat_menu.get()

 

        if self.editing_name:
            error = self.manager.update_habit(
                self.editing_name, name, desc, freq, cat
            )
        else:
            error = self.manager.add_habit(name, desc, freq, cat)

 

        if error:
            self.error_lbl.configure(text=error)
            return

 

        self.clear()
        self.refresh()

 

    def start_edit(self, h):
        self.editing_name = h["name"]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, h["name"])
        self.desc_entry.delete(0, "end")
        self.desc_entry.insert(0, h["description"])
        self.freq_menu.set(h["frequency"])
        self.cat_menu.set(h["category"])
        self.submit_btn.configure(text="Speichern")

 

    def clear(self):
        self.editing_name = None
        self.name_entry.delete(0, "end")
        self.desc_entry.delete(0, "end")
        self.cat_menu.set("Normal")
        self.submit_btn.configure(text="Hinzufügen")
        self.error_lbl.configure(text="")

 

    def set_done(self, name, done):
        self.manager.set_done(name, done)
        self.refresh()

 

    def delete(self, name):
        self.manager.delete_habit(name)
        self.refresh()