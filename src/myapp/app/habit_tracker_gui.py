import customtkinter as ctk
from tkinter import messagebox


class HabitTrackerGUI(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.title("Habit Tracker")
        self.geometry("820x560")
        self.resizable(False, False)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_header()
        self._create_list()
        self._create_xp_bar()
        self._refresh()

    # ---------- HEADER ----------
    def _create_header(self):
        frame = ctk.CTkFrame(self, height=60)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(
            frame,
            text="📅 Habit Tracker",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            frame,
            text="+ Neues Habit",
            command=self._open_add_habit
        ).pack(side="right", padx=20)

    # ---------- LIST ----------
    def _create_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=10)

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for habit in self.manager.get_habits():
            self._habit_row(habit)

        self._update_xp_bar()

    def _habit_row(self, habit):
        row = ctk.CTkFrame(self.list_frame)
        row.pack(fill="x", pady=6, padx=6)

        text_frame = ctk.CTkFrame(row, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True, padx=10)

        ctk.CTkLabel(
            text_frame,
            text=habit["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_frame,
            text=f'{habit["description"]} • {habit["frequency"]}',
            text_color="gray"
        ).pack(anchor="w")

        btn_frame = ctk.CTkFrame(row, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        status = "🟢 Erledigt" if habit["is_done_today"] else "🔴 Offen"
        ctk.CTkLabel(btn_frame, text=status, width=90).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame,
            text="✔",
            width=40,
            command=lambda: self._set_done(habit["name"], True)
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_frame,
            text="✖",
            width=40,
            fg_color="#555555",
            command=lambda: self._set_done(habit["name"], False)
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_frame,
            text="✏️",
            width=40,
            command=lambda: self._open_edit_habit(habit)
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            btn_frame,
            text="🗑",
            width=40,
            fg_color="#8b0000",
            hover_color="#b22222",
            command=lambda: self._delete(habit["name"])
        ).pack(side="left", padx=4)

    # ---------- XP ----------
    def _create_xp_bar(self):
        frame = ctk.CTkFrame(self, height=60)
        frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        self.level_label = ctk.CTkLabel(frame)
        self.level_label.pack()

        self.xp_bar = ctk.CTkProgressBar(frame, width=520)
        self.xp_bar.pack(pady=6)

    def _update_xp_bar(self):
        self.level_label.configure(
            text=f"Level {self.manager.get_level()} • Gesamt-XP: {self.manager.get_total_xp()}"
        )
        self.xp_bar.set(self.manager.get_xp_progress())

    # ---------- ACTIONS ----------
    def _set_done(self, name, done):
        if done:
            messagebox.showinfo("XP erhalten", "+10 XP 🎉")
        self.manager.set_habit_done(name, done)
        self._refresh()

    def _delete(self, name):
        if messagebox.askyesno("Löschen", f"{name} löschen?"):
            self.manager.delete_habit(name)
            self._refresh()

    def _open_add_habit(self):
        self._open_habit_editor()

    def _open_edit_habit(self, habit):
        self._open_habit_editor(habit)

    def _open_habit_editor(self, habit=None):
        win = ctk.CTkToplevel(self)
        win.title("Habit bearbeiten" if habit else "Neues Habit")
        win.geometry("400x360")
        win.grab_set()

        name = ctk.CTkEntry(win, placeholder_text="Name")
        name.pack(pady=10, padx=20, fill="x")

        desc = ctk.CTkEntry(win, placeholder_text="Beschreibung")
        desc.pack(pady=10, padx=20, fill="x")

        freq_var = ctk.StringVar(value="daily")
        freq_menu = ctk.CTkOptionMenu(
            win,
            values=["daily", "weekly", "monthly"],
            variable=freq_var
        )
        freq_menu.pack(pady=10)

        if habit:
            name.insert(0, habit["name"])
            desc.insert(0, habit["description"])
            freq_var.set(habit["frequency"])

        def save():
            if habit:
                self.manager.update_habit(
                    habit["name"],
                    name.get(),
                    desc.get(),
                    freq_var.get()
                )
            else:
                self.manager.add_habit(
                    name.get(),
                    desc.get(),
                    freq_var.get()
                )
            win.destroy()
            self._refresh()

        ctk.CTkButton(win, text="Speichern", command=save).pack(pady=20)
