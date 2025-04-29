import customtkinter as ctk

class PomodoroFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")

        =
        header = ctk.CTkFrame(self, height=80, fg_color="white")
        header.pack(side="top", fill="x")
        ctk.CTkLabel(
            master=header,
            text="Pomodoro Timer",
            fg_color="red",
            text_color="white",
            font=("Inter", 40, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")

        
        content = ctk.CTkFrame(self, fg_color="white")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        # Pomodoro funcitons
        self.sessions = [("Work", 1 * 3), ("Break", 1 * 3)]  
        self.session_index = 0
        self.time_left = self.sessions[self.session_index][1]
        self.running = False
        self.session_counter = 0

        self.session_label = ctk.CTkLabel(content, text="Work Session", font=("Inter", 80), text_color="#2E86C1")
        self.session_label.pack(pady=30)

        self.timer_label = ctk.CTkLabel(content, text=self._format_time(self.time_left), font=("Inter", 100), text_color="#A3A1A1")
        self.timer_label.pack(pady=20)

        self.counter_label = ctk.CTkLabel(content, text=f"Sessions Completed: {self.session_counter}", font=("Inter", 24), text_color="#555555")
        self.counter_label.pack(pady=10)

        # Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(
            btn_frame, text="Start", width=200, height=80,
            font=("Inter", 30, "bold"), fg_color="#A3A1A1",
            hover_color="#8F8D8D", text_color="white",
            command=self.start_timer
        )
        self.start_button.pack(side="left", padx=20)

        self.reset_button = ctk.CTkButton(
            btn_frame, text="Reset", width=200, height=80,
            font=("Inter", 30, "bold"), fg_color="#A3A1A1",
            hover_color="#8F8D8D", text_color="white",
            command=self.reset_timer
        )
        self.reset_button.pack(side="left", padx=20)

        self.status_label = ctk.CTkLabel(content, text="Ready", font=("Inter", 20), text_color="#888888")
        self.status_label.pack(pady=10)

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
            self.counter_label.configure(text=f"Sessions Completed: {self.session_counter}")

        self.session_index = (self.session_index + 1) % len(self.sessions)
        name, duration = self.sessions[self.session_index]
        self.time_left = duration
        self._update_session_label()
        self.timer_label.configure(text=self._format_time(self.time_left))
        self.status_label.configure(text=f"{name} starting...")

    def _update_session_label(self):
        name = self.sessions[self.session_index][0]
        if name == "Work":
            self.session_label.configure(text="Work Session", text_color="#2E86C1")
        else:
            self.session_label.configure(text="Break Time", text_color="#27AE60")
