import customtkinter as ctk

# Set theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def habit_builder_page(main_content):
    # Clear current content
    for widget in main_content.winfo_children():
        widget.destroy()

    # === Habit Builder Layout ===
    title = ctk.CTkLabel(main_content, text="Habit builder", font=ctk.CTkFont(size=48, weight="bold"), text_color="black")
    title.pack(anchor="nw", padx=20, pady=(20, 10))

    create_btn = ctk.CTkButton(main_content, text="Create new habit +", fg_color="#d9d9d9", text_color="black", hover_color="#cccccc")
    create_btn.pack(anchor="nw", padx=20, pady=(0, 20))

    # Habit Card
    habit_card = ctk.CTkFrame(main_content, fg_color="#d9d9d9", corner_radius=10)
    habit_card.pack(anchor="nw", padx=20, pady=10, fill="x")

    habit_title = ctk.CTkLabel(habit_card, text="Exercise", font=ctk.CTkFont(size=24, slant="italic"), text_color="white")
    habit_title.pack(anchor="nw", padx=10, pady=(10, 0))

    habit_subtext = ctk.CTkLabel(habit_card, text="10 mins atleast -", font=ctk.CTkFont(size=16), text_color="white")
    habit_subtext.pack(anchor="nw", padx=10, pady=(0, 10))

    # Day labels
    days_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
    days_frame.pack(anchor="nw", padx=10, pady=10)

    days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
    for day in days:
        day_label = ctk.CTkLabel(days_frame, text=day, text_color="white", font=ctk.CTkFont(size=14))
        day_label.pack(side="left", padx=10)

    # Circles for tracking
    circle_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
    circle_frame.pack(anchor="nw", padx=10, pady=(0, 10))

    circle_colors = ["#7d6b6b", "#d1b5b5", "#d1b5b5", "#7d6b6b", "#7d6b6b", "#7d6b6b", "#7d6b6b"]

    for color in circle_colors:
        circle = ctk.CTkButton(circle_frame, text="", width=30, height=30, corner_radius=15, fg_color=color, hover=False, state="disabled")
        circle.pack(side="left", padx=10)

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

    # Main content area
    main_content = ctk.CTkFrame(root2, fg_color="white")
    main_content.pack(side="left", expand=True, fill="both")

    # Sidebar button functions
    def go_to_home():
        print("Navigating to Home...")
        # Example home content
        for widget in main_content.winfo_children():
            widget.destroy()
        ctk.CTkLabel(main_content, text="Home Page", font=("Inter", 24, "bold")).pack(pady=20)

    def goal_planner():
        print("Opening Goal Planner...")
        for widget in main_content.winfo_children():
            widget.destroy()
        ctk.CTkLabel(main_content, text="Goal Planner Page", font=("Inter", 24, "bold")).pack(pady=20)

    def habit_builder():
        print("Launching Habit Builder...")
        habit_builder_page(main_content)

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

    # Default page on startup = Home
    go_to_home()

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
             font=("Inter", 20, "bold"), height=10).pack(fill="x")

e1 = ctk.CTkEntry(root1, width=300, font=("Inter", 14), placeholder_text="Your Username")
e1.pack(pady=20)

e2 = ctk.CTkEntry(root1, width=300, font=("Inter", 14), placeholder_text="Your Password", show="*")
e2.pack(pady=20)

ctk.CTkButton(root1, text="Login", fg_color="#FF5722", hover_color="#E64A19",
              text_color="white", font=("Inter", 14, "bold"),
              command=login).pack(pady=20)

root1.mainloop()
