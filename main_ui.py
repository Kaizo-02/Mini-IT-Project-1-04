import customtkinter as ctk

# Set theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def main_window():
    global root2
    root2 = ctk.CTk()
    root2.title("IMPROVE - MAKE LIFE BETTER")
    root2.geometry("1920x1080")

    # Header
    header = ctk.CTkFrame(root2, fg_color="white", height=80)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="IMPROVE - MAKE LIFE BETTER",
                 fg_color="#FF5722", text_color="white",
                 font=("Inter", 24, "bold"),
                 height=80).pack(fill="both")

    # Sidebar
    sidebar = ctk.CTkFrame(root2, fg_color="#FF5722", width=200)
    sidebar.pack(side="left", fill="y")

    ctk.CTkLabel(sidebar, text="Main Menu", fg_color="#FF5722",
                 text_color="black", font=("Inter", 20, "bold")).pack(pady=20)

    def go_to_home():
        print("Navigating to Home...")

    def goal_planner():
        print("Opening Goal Planner...")

    def habit_builder():
        print("Launching Habit Builder...")

    def pomodoro_timer():
        print("Starting Pomodoro Timer...")
        root2.withdraw()
        from pomodorocoding import PomodoroApp
        app = PomodoroApp()
        app.mainloop()
        root2.deiconify()

    buttons = [
        {"text": "Home", "command": go_to_home},
        {"text": "Goal Planner", "command": goal_planner},
        {"text": "Habit Builder", "command": habit_builder},
        {"text": "Pomodoro Timer", "command": pomodoro_timer}
    ]

    for btn in buttons:
        button = ctk.CTkButton(sidebar, text=btn["text"],
                                fg_color="#A3A1A1", hover_color="#E64A19",
                                text_color="white",
                                font=("Inter", 16, "bold"),
                                corner_radius=5,
                                command=btn["command"])
        button.pack(pady=10, fill="x", padx=10)

    # Main content area
    main_content = ctk.CTkFrame(root2, fg_color="white")
    main_content.pack(side="left", expand=True, fill="both")

    sections = [
        {"title": "Your Planner Progression"},
        {"title": "Weekly Habit Track"},
        {"title": "Pomodoro Timer - Build Your Focus"},
        {"title": "Got Something in Mind? Write it Down."}
    ]

    for sec in sections:
        section_frame = ctk.CTkFrame(main_content, fg_color="#FFEBEE",
                                      border_color="#FFCDD2", border_width=2)
        section_frame.pack(padx=20, pady=20, fill="x")

        ctk.CTkButton(section_frame, text=sec["title"],
                      fg_color="white", hover_color="#f0f0f0",
                      text_color="black",
                      font=("Times New Roman", 18, "bold"),
                      corner_radius=5).pack(anchor="w", padx=10, pady=10)

    root2.mainloop()

def login():
    username = e1.get()
    password = e2.get()
    print(f"Username: {username}, Password: {password}")
    root1.destroy()
    main_window()

# Login window
root1 = ctk.CTk()
root1.title("IMPROVE - MAKE LIFE BETTER")
root1.geometry("700x500")

ctk.CTkLabel(root1, text="Welcome to IMPROVE",
             fg_color="#FF5722", text_color="white",
             font=("Inter", 20, "bold"), height=50).pack(fill="x")

e1 = ctk.CTkEntry(root1, width=300, font=("Inter", 14), placeholder_text="Your Username")
e1.pack(pady=20)

e2 = ctk.CTkEntry(root1, width=300, font=("Inter", 14), placeholder_text="Your Password", show="*")
e2.pack(pady=20)

ctk.CTkButton(root1, text="Login", fg_color="#FF5722", hover_color="#E64A19",
              text_color="white", font=("Inter", 14, "bold"),
              command=login).pack(pady=20)

root1.mainloop()
