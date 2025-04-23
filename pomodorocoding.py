import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class PomodoroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timer")
        self.geometry("400x550")
        self.resizable(False, False)

        # Pomodoro Settings
        self.sessions = [("Work", 25 * 60), ("Break", 5 * 60)]
        self.session_index = 0
        self.time_left = self.sessions[self.session_index][1]
        self.running = False

        # --- UI ---
        self.session_label = ctk.CTkLabel(self, text="Work Session", font=("Helvetica", 20))
        self.session_label.pack(pady=30)

        self.timer_label = ctk.CTkLabel(self, text=self.format_time(self.time_left), font=("Helvetica", 64))
        self.timer_label.pack(pady=20)

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_timer, width=120)
        self.start_button.pack(pady=10)

        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.reset_timer, width=120)
        self.reset_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Ready", font=("Helvetica", 14), text_color="#888")
        self.status_label.pack(pady=10)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def start_timer(self):
        if not self.running:
            self.running = True
            self.status_label.configure(text="Running...")
            self.countdown()

    def countdown(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.configure(text=self.format_time(self.time_left))
            self.after(1000, self.countdown)
        elif self.running:
            self.running = False
            self.status_label.configure(text="Session Complete!")
            self.switch_session()

    def reset_timer(self):
        self.running = False
        self.time_left = self.sessions[self.session_index][1]
        self.timer_label.configure(text=self.format_time(self.time_left))
        self.status_label.configure(text="Reset")
        self.update_session_label()

    def switch_session(self):
        self.session_index = (self.session_index + 1) % len(self.sessions)
        session_name, duration = self.sessions[self.session_index]
        self.time_left = duration
        self.update_session_label()
        self.timer_label.configure(text=self.format_time(self.time_left))
        self.status_label.configure(text=f"{session_name} starting...")

    def update_session_label(self):
        session_name = self.sessions[self.session_index][0]
        if session_name == "Work":
            self.session_label.configure(text="Work Session", text_color="#2E86C1")
        else:
            self.session_label.configure(text="Break Time", text_color="#27AE60")

if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()
