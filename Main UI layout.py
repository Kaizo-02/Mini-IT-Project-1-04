from tkinter import *
from tkinter.ttk import Separator
from pomodorocoding import PomodoroApp
from models import add_user, get_users, add_goal, get_goals, add_habit, get_habits, add_timers, timers
from argon2 import PasswordHasher

ph = PasswordHasher()

# Global variables
e1, e2, e3 = None, None, None
root1 = None

def clear_placeholder(event, entry, placeholder, is_password=False):
    if entry.get() == placeholder:
        entry.delete(0, END)
        if is_password:
            entry.config(show="*")

def add_placeholder(entry, placeholder, is_password=False):
    if not entry.get():
        entry.insert(0, placeholder)
        if is_password:
            entry.config(show="")

def login():
    username = e1.get()
    password = e2.get()

    users = get_users()
    for user in users:
        db_username = user[1]
        db_hashed_password = user[3]
        if username == db_username:
            try:
                ph.verify(db_hashed_password, password)
                print("Login successful!")
                root1.destroy()
                main_window(user[0])
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
    for widget in root1.winfo_children():
        widget.destroy()

    Label(root1, text="Welcome to IMPROVE", bg="#FF5722", fg="white", font=("Arial", 20, "bold"), height=2).pack(fill="x")

    global e1, e2
    e1 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2)
    e1.pack(pady=20)
    e1.insert(0, "Your Username")
    e1.bind("<FocusIn>", lambda event: clear_placeholder(event, e1, "Your Username"))
    e1.bind("<FocusOut>", lambda event: add_placeholder(e1, "Your Username"))

    e2 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2)
    e2.pack(pady=20)
    e2.insert(0, "Your Password")
    e2.bind("<FocusIn>", lambda event: clear_placeholder(event, e2, "Your Password", is_password=True))
    e2.bind("<FocusOut>", lambda event: add_placeholder(e2, "Your Password", is_password=True))

    Button(root1, text="Login", bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0, command=login).pack(pady=20)
    Button(root1, text="Register", bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0, command=show_register).pack(pady=10)

def show_register():
    for widget in root1.winfo_children():
        widget.destroy()

    Label(root1, text="Register for IMPROVE", bg="#FF5722", fg="white", font=("Arial", 20, "bold"), height=2).pack(fill="x")

    global e1, e2, e3
    e1 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2)
    e1.pack(pady=10)
    e1.insert(0, "Choose a Username")
    e1.bind("<FocusIn>", lambda event: clear_placeholder(event, e1, "Choose a Username"))
    e1.bind("<FocusOut>", lambda event: add_placeholder(e1, "Choose a Username"))

    e3 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2)
    e3.pack(pady=10)
    e3.insert(0, "Your Email")
    e3.bind("<FocusIn>", lambda event: clear_placeholder(event, e3, "Your Email"))
    e3.bind("<FocusOut>", lambda event: add_placeholder(e3, "Your Email"))

    e2 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2)
    e2.pack(pady=10)
    e2.insert(0, "Choose a Password")
    e2.bind("<FocusIn>", lambda event: clear_placeholder(event, e2, "Choose a Password", is_password=True))
    e2.bind("<FocusOut>", lambda event: add_placeholder(e2, "Choose a Password", is_password=True))

    Button(root1, text="Register", bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0, command=save_user).pack(pady=20)
    Button(root1, text="Back to Login", bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0, command=show_login).pack(pady=10)

def login_window():
    global root1
    root1 = Tk()
    root1.title("IMPROVE - MAKE LIFE BETTER")
    root1.geometry("700x500")
    root1.configure(bg="#f5f5f5")
    show_login()
    root1.mainloop()

def main_window(user_id):
    root2 = Tk()
    root2.title("IMPROVE - MAKE LIFE BETTER")
    root2.geometry("1420x1010")
    root2.configure(bg="#f5f5f5")

    header = Frame(root2, bg="white", height=80)
    header.pack(fill="x")
    Label(header, text="IMPROVE - MAKE LIFE BETTER", bg="#FF5722", fg="white", font=("Arial", 24, "bold")).pack(pady=20)

    sidebar = Frame(root2, bg="#FF5722", width=200)
    sidebar.pack(side="left", fill="y")

    def on_hover(event): event.widget.config(bg="#E64A19")
    def on_leave(event): event.widget.config(bg="#FF5722")

    def go_to_home(): print("Navigating to Home...")
    def goal_planner(): print("Opening Goal Planner...")
    def habit_builder(): print("Launching Habit Builder...")
    def pomodoro_timer():
        print("Starting Pomodoro Timer...")
        PomodoroApp().mainloop()

    buttons = [
        {"text": "Home", "command": go_to_home},
        {"text": "Goal Planner", "command": goal_planner},
        {"text": "Habit Builder", "command": habit_builder},
        {"text": "Pomodoro Timer", "command": pomodoro_timer}
    ]

    for btn in buttons:
        b = Button(sidebar, text=btn["text"], bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0, command=btn["command"])
        b.pack(pady=10, fill="x", padx=10)
        b.bind("<Enter>", on_hover)
        b.bind("<Leave>", on_leave)

    main_content = Frame(root2, bg="white", width=215)
    main_content.pack(side="right", expand=True, fill="both")

    sections = [
        "Your Planner Progression",
        "Weekly Habit Track",
        "Pomodoro Timer - Build Your Focus",
        "Got Something in Mind? Write it Down."
    ]

    for title in sections:
        section_frame = Frame(main_content, bg="#FFEBEE", highlightbackground="#FFCDD2", highlightthickness=2, padx=20, pady=20)
        section_frame.pack(padx=20, pady=20, fill="x")
        Button(section_frame, text=title, bg="#FFFFFF", font=("Times New Roman", 18, "bold"), relief="flat").pack(anchor="w")

    root2.mainloop()

# Start the app
login_window()
