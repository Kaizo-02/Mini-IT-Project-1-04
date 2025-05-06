import customtkinter as ctk
from pomodorocoding import PomodoroApp
from models import add_user, get_users, add_goal, get_goals, add_habit, get_habits, add_timers, timers
from argon2 import PasswordHasher

ph = PasswordHasher()

# Global state
e1, e2, e3 = None, None, None
app = None

def clear_placeholder(event, entry, placeholder, is_password=False):
    if entry.get() == placeholder:
        entry.delete(0, ctk.END)
        if is_password:
            entry.configure(show="*")

def add_placeholder(entry, placeholder, is_password=False):
    if not entry.get():
        entry.insert(0, placeholder)
        if is_password:
            entry.configure(show="")

def login():
    username = e1.get()
    password = e2.get()
    users = get_users()

    for user in users:
        if username == user[1]:
            try:
                ph.verify(user[3], password)
                print("Login successful!")
                show_main(user[0])
                return
            except:
                print("Password verification failed.")
                return
    print("User not found.")

def save_user():
    username = e1.get()
    email = e3.get()
    password = e2.get()
    try:
        hashed_password = ph.hash(password)
        add_user(username, email, hashed_password)
        print("User registered successfully!")
        show_login()
    except Exception as e:
        print(f"Error during registration: {e}")

def show_login():
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkLabel(app, text="Welcome to IMPROVE", text_color="white",
                 font=ctk.CTkFont(size=20, weight="bold"), height=50, fg_color="#FF5722").pack(fill="x")

    global e1, e2
    e1 = ctk.CTkEntry(app, width=300, font=("Arial", 14))
    e1.pack(pady=15)
    e1.insert(0, "Your Username")
    e1.bind("<FocusIn>", lambda e: clear_placeholder(e, e1, "Your Username"))
    e1.bind("<FocusOut>", lambda e: add_placeholder(e1, "Your Username"))

    e2 = ctk.CTkEntry(app, width=300, font=("Arial", 14))
    e2.pack(pady=15)
    e2.insert(0, "Your Password")
    e2.bind("<FocusIn>", lambda e: clear_placeholder(e, e2, "Your Password", True))
    e2.bind("<FocusOut>", lambda e: add_placeholder(e2, "Your Password", True))

    ctk.CTkButton(app, text="Login", command=login,
                  fg_color="#FF5722", text_color="white", font=("Arial", 14, "bold")).pack(pady=15)
    ctk.CTkButton(app, text="Register", command=show_register,
                  fg_color="#FF5722", text_color="white", font=("Arial", 14, "bold")).pack(pady=5)

def show_register():
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkLabel(app, text="Register for IMPROVE", text_color="white",
                 font=ctk.CTkFont(size=20, weight="bold"), height=50, fg_color="#FF5722").pack(fill="x")

    global e1, e2, e3
    e1 = ctk.CTkEntry(app, width=300, font=("Arial", 14))
    e1.pack(pady=10)
    e1.insert(0, "Choose a Username")
    e1.bind("<FocusIn>", lambda e: clear_placeholder(e, e1, "Choose a Username"))
    e1.bind("<FocusOut>", lambda e: add_placeholder(e1, "Choose a Username"))

    e3 = ctk.CTkEntry(app, width=300, font=("Arial", 14))
    e3.pack(pady=10)
    e3.insert(0, "Your Email")
    e3.bind("<FocusIn>", lambda e: clear_placeholder(e, e3, "Your Email"))
    e3.bind("<FocusOut>", lambda e: add_placeholder(e3, "Your Email"))

    e2 = ctk.CTkEntry(app, width=300, font=("Arial", 14))
    e2.pack(pady=10)
    e2.insert(0, "Choose a Password")
    e2.bind("<FocusIn>", lambda e: clear_placeholder(e, e2, "Choose a Password", True))
    e2.bind("<FocusOut>", lambda e: add_placeholder(e2, "Choose a Password", True))

    ctk.CTkButton(app, text="Register", command=save_user,
                  fg_color="#FF5722", text_color="white", font=("Arial", 14, "bold")).pack(pady=15)
    ctk.CTkButton(app, text="Back to Login", command=show_login,
                  fg_color="#FF5722", text_color="white", font=("Arial", 14, "bold")).pack(pady=5)

def show_main(user_id):
    for widget in app.winfo_children():
        widget.destroy()

    header = ctk.CTkFrame(app, height=80)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="IMPROVE - MAKE LIFE BETTER", text_color="white",
                 fg_color="#FF5722", corner_radius=0, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

    content = ctk.CTkFrame(app)
    content.pack(fill="both", expand=True)

    sidebar = ctk.CTkFrame(content, width=200, fg_color="#FF5722")
    sidebar.pack(side="left", fill="y")

    main_area = ctk.CTkFrame(content, fg_color="white")
    main_area.pack(side="right", fill="both", expand=True)

    def go_to_home():
        print("Navigating to Home...")
        for widget in main_area.winfo_children():
            widget.destroy()

    def goal_planner():
        print("Opening Goal Planner...")
        for widget in main_area.winfo_children():
            widget.destroy()

    def habit_builder():
        print("Launching Habit Builder...")
        for widget in main_area.winfo_children():
            widget.destroy()

    def pomodoro_timer():
        print("Starting Pomodoro Timer...")
        for widget in main_area.winfo_children():
            widget.destroy()
        PomodoroApp(master=main_area)

    buttons = [
        ("Home", go_to_home),
        ("Goal Planner", goal_planner),
        ("Habit Builder", habit_builder),
        ("Pomodoro Timer", pomodoro_timer)
    ]

    for txt, cmd in buttons:
        ctk.CTkButton(sidebar, text=txt, command=cmd,
                      fg_color="#F4511E", hover_color="#D84315",
                      text_color="white", font=("Arial", 14)).pack(pady=10, fill="x", padx=10)

    sections = [
        "Your Planner Progression",
        "Weekly Habit Track",
        "Pomodoro Timer - Build Your Focus",
        "Got Something in Mind? Write it Down."
    ]

    for section in sections:
        frame = ctk.CTkFrame(main_area, fg_color="#FFEBEE", border_color="#FFCDD2", border_width=2)
        frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkButton(frame, text=section, fg_color="white", text_color="black",
                      font=ctk.CTkFont(family="Times New Roman", size=18, weight="bold"), hover=False).pack(anchor="w", padx=20, pady=10)

def run_app():
    global app
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("IMPROVE - MAKE LIFE BETTER")
    app.geometry("1000x700")
    show_login()
    app.mainloop()

run_app()
