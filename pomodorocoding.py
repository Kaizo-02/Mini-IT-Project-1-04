import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class ImproveApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("IMPROVE - MAKE LIFE BETTER")
        self.geometry("900x600")
        self.resizable(True, True)

        # 📌 HEADER (White Background & Black Title)
        header = ctk.CTkFrame(self, height=50, fg_color="white")
        header.pack(fill="x")
        
        ctk.CTkLabel(
            master=header,
            text="IMPROVE - MAKE LIFE BETTER",
            text_color="black",
            font=("Inter", 30, "bold")
        ).pack(pady=10)

        # 📌 SIDEBAR NAVIGATION
        sidebar = ctk.CTkFrame(self, width=200, fg_color="#FF5722")
        sidebar.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            master=sidebar, text="Menu", text_color="black", font=("Inter", 20, "bold")
        ).pack(pady=20)

        # 📌 MAIN CONTENT AREA (Frame Switching)
        self.main_content = ctk.CTkFrame(self, fg_color="white")
        self.main_content.pack(side="right", expand=True, fill="both")

        # 📌 Define Frames for Different Features
        self.home_frame = self.create_home_frame()
        self.goal_planner_frame = self.create_goal_planner_frame()
        self.pomodoro_frame = self.create_pomodoro_frame()

        # 📌 Sidebar Buttons (Navigation)
        menu_options = [
            {"text": "Home", "command": self.show_home},
            {"text": "Goal Planner", "command": self.show_goal_planner},
            {"text": "Pomodoro Timer", "command": self.show_pomodoro},
        ]

        for option in menu_options:
            ctk.CTkButton(
                master=sidebar, text=option["text"], text_color="black", 
                fg_color="lightgray", hover_color="#FF7043", font=("Inter", 18),
                command=option["command"]
            ).pack(pady=10, padx=10, fill="x")

        # 📌 Show Home Page First
        self.show_home()

    # 📌 Home Page (Progression & Diary)
    def create_home_frame(self):
        frame = ctk.CTkFrame(self.main_content, fg_color="#FFEBEE", padx=20, pady=20)
        sections = [
            "Your Planner Progression",
            "Weekly Habit Track",
            "Pomodoro Timer - Build Your Focus",
            "Got Something in Mind? Write it Down."
        ]
        for sec in sections:
            ctk.CTkButton(master=frame, text=sec, fg_color="white", text_color="black",
                          font=("Inter", 18, "bold"), command=lambda: print(f"Opening {sec}")).pack(pady=10, fill="x")
        return frame

    # 📌 Goal Planner Page
    def create_goal_planner_frame(self):
        frame = ctk.CTkFrame(self.main_content, fg_color="#FFEBEE", padx=20, pady=20)
        ctk.CTkLabel(frame, text="Goal Planner", font=("Inter", 18, "bold")).pack()
        ctk.CTkEntry(frame, width=300, placeholder_text="Enter Goal").pack(pady=5)
        ctk.CTkEntry(frame, width=300, placeholder_text="Due Date (DD/MM/YYYY)").pack(pady=5)
        ctk.CTkButton(frame, text="Add Goal", fg_color="green").pack(pady=10)
        return frame

    # 📌 Pomodoro Timer Page
    def create_pomodoro_frame(self):
        frame = ctk.CTkFrame(self.main_content, fg_color="white", padx=20, pady=20)

        self.sessions = [("Work", 25 * 60), ("Break", 5 * 60)]
        self.session_index = 0
        self.time_left = self.sessions[self.session_index][1]
        self.running = False
        self.session_counter = 0

        self.session_label = ctk.CTkLabel(frame, text="Work Session", font=("Inter", 24, "bold"))
        self.session_label.pack(pady=10)

        self.timer_label = ctk.CTkLabel(frame, text=self._format_time(self.time_left), font=("Inter", 40, "bold"))
        self.timer_label.pack(pady=10)

        self.counter_label = ctk.CTkLabel(frame, text=f"Sessions Completed: {self.session_counter}", font=("Inter", 18))
        self.counter_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Start", fg_color="green", command=self.start_timer).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Reset", fg_color="red", command=self.reset_timer).pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(frame, text="Ready", font=("Inter", 18))
        self.status_label.pack(pady=10)

        return frame

    # 📌 Functions to Switch Sections
    def show_home(self):
        self._switch_frame(self.home_frame)

    def show_goal_planner(self):
        self._switch_frame(self.goal_planner_frame)

    def show_pomodoro(self):
        self._switch_frame(self.pomodoro_frame)

    def _switch_frame(self, frame):
        for widget in self.main_content.winfo_children():
            widget.pack_forget()
        frame.pack(expand=True, fill="both")

    # 📌 Timer Functions
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
        self.time_left = self.sessions[self.session_index][1]
        self._update_session_label()
        self.timer_label.configure(text=self._format_time(self.time_left))
        self.status_label.configure(text=f"{self.sessions[self.session_index][0]} starting...")

    def _update_session_label(self):
        name = self.sessions[self.session_index][0]
        self.session_label.configure(text=f"{name} Session")

# Run the App
if __name__ == "__main__":
    app = ImproveApp()
    app.mainloop()
