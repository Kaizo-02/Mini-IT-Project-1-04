import customtkinter as ctk
  
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IMPROVE - MAKE LIFE BETTER")
        self.geometry("1920x1080")
        self.resizable(True, True)
        self.grid_rowconfigure(0, weight=1)  # content row expands
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(master=self, height=50, fg_color="white")
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        ctk.CTkLabel(
            master=header,
            text="IMPROVE - MAKE LIFE BETTER",
            fg_color="red",
            text_color="white",
            font=("Inter", 70, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Sidebar
        sidebar = ctk.CTkFrame(master=self, width=200, fg_color="red")
        sidebar.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        for name in ["Home", "Goal Planner", "Habit builder", "Pomodoro timer"]:
            ctk.CTkButton(
                master=sidebar,
                text=name,
                fg_color="lightgray",
                hover_color="#FF7043",
                text_color="black",
                font=("Inter", 25, "bold"),
                border_width=2,
                command=lambda t=name: self.on_menu(t)
            ).pack(pady=(20, 0), padx=10, fill="x")

        # Main Content
        content = ctk.CTkFrame(master=self, fg_color="white")
        content.grid(row=1, column=1, sticky="nsew")

        self.sessions = [("Work", 1 * 3), ("Break", 1 * 3)]
        self.session_index = 0
        self.time_left = self.sessions[self.session_index][1]
        self.running = False
        self.session_counter = 0

        self.session_label = ctk.CTkLabel(
            master=content,
            text="Work Session",
            font=("Inter", 150 , "bold"),
            text_color="#2E86C1"
        )
        self.session_label.pack(pady=30)

        self.timer_label = ctk.CTkLabel(
            master=content,
            text=self._format_time(self.time_left),
            font=("Inter", 200),
            text_color="#A3A1A1"
        )
        self.timer_label.pack(pady=20)

        self.counter_label = ctk.CTkLabel(
            master=content,
            text=f"Sessions Completed: {self.session_counter}",
            font=("Inter", 24),
            text_color="#555555"
        )
        self.counter_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(master=content, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(
            master=btn_frame,
            text="Start",
            width=300,
            height=100,
            font=("Inter", 30, "bold"),
            fg_color="#A3A1A1",
            hover_color="#8F8D8D",
            text_color="white",
            command=self.start_timer
        )
        self.start_button.pack(side="left", padx=20)

        self.reset_button = ctk.CTkButton(
            master=btn_frame,
            text="Reset",
            width=300,
            height=100,
            font=("Inter", 30, "bold"),
            fg_color="#A3A1A1",
            hover_color="#8F8D8D",
            text_color="white",
            command=self.reset_timer
        )
        self.reset_button.pack(side="left", padx=20)

        self.status_label = ctk.CTkLabel(
            master=content,
            text="Ready",
            font=("Inter", 20),
            text_color="#888888"
        )
        self.status_label.pack(pady=10)

    def on_menu(self, selection):
        if selection == "Home":
            self.destroy()
            from main_ui import main_window
            main_window()
        else:
            print(f"Menu clicked: {selection}")

    def _format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def start_timer(self):
        if not self.running:
            self.running = True
            self.status_label.configure(text="Running...")
            self._countdown()

    def _countdown(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.configure(text=self._format_time(self.time_left))
            self.after(1000, self._countdown)
        elif self.running:
            self.running = False
            self.status_label.configure(text="Session Complete!")
            self._switch_session()

    def reset_timer(self):
        self.running = False
        self.time_left = self.sessions[self.session_index][1]
        self.timer_label.configure(text=self._format_time(self.time_left))
        self.status_label.configure(text="Reset")
        self._update_session_label()

    def _switch_session(self):
        if self.sessions[self.session_index][0] == "Work":
            self.session_counter += 1
            self.counter_label.configure(
                text=f"Sessions Completed: {self.session_counter}"
            )
        self.session_index = (self.session_index + 1) % len(self.sessions)
        name, duration = self.sessions[self.session_index]
        self.time_left = duration
        self._update_session_label()
        self.timer_label.configure(text=self._format_time(self.time_left))
        self.status_label.configure(text=f"{name} starting...")

    def _update_session_label(self):
        name = self.sessions[self.session_index][0]
        if name == "Work":
            self.session_label.configure(text="Work Session", text_color="#A3A1A1")
        else:
            self.session_label.configure(text="Break Time", text_color="#27AE60")