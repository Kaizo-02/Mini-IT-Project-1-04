import customtkinter as ctk
from pomodorocoding import PomodoroApp
from models import add_user, get_users, add_goal, get_goals, add_habit, get_habits
from argon2 import PasswordHasher

ph = PasswordHasher()

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

    # Header
    header = ctk.CTkFrame(app, height=60, fg_color="#FF5722")
    header.pack(fill="x")

    hamburger_btn = ctk.CTkButton(header, text="☰", width=50, command=lambda: toggle_sidebar(), fg_color="white", text_color="black")
    hamburger_btn.pack(side="left", padx=10, pady=10)

    title = ctk.CTkLabel(header, text="IMPROVE - MAKE LIFE BETTER", font=ctk.CTkFont(size=20, weight="bold"), text_color="white", fg_color="#FF5722")
    title.pack(pady=10)

    # Wrapper
    wrapper = ctk.CTkFrame(app)
    wrapper.pack(fill="both", expand=True)

    # Sidebar
    sidebar = ctk.CTkFrame(wrapper, width=0, fg_color="#FF5722")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Main Area
    main_area = ctk.CTkFrame(wrapper, fg_color="white")
    main_area.pack(side="right", fill="both", expand=True)

    sidebar_state = {"visible": False}

    def toggle_sidebar():
        if sidebar_state["visible"]:
            slide_out()
        else:
            slide_in()

    def slide_in(current=0):
        if current < 200:
            sidebar.configure(width=current)
            app.after(5, lambda: slide_in(current + 20))
        else:
            sidebar.configure(width=200)
            sidebar_state["visible"] = True

    def slide_out(current=200):
        if current > 0:
            sidebar.configure(width=current)
            app.after(5, lambda: slide_out(current - 20))
        else:
            sidebar.configure(width=0)
            sidebar_state["visible"] = False

    def clear_main_area():
        for widget in main_area.winfo_children():
            widget.destroy()

    def go_to_home():
        clear_main_area()
        ctk.CTkLabel(main_area, text="Home Page", font=("Arial", 18, "bold")).pack(pady=10)

    def goal_planner():
        clear_main_area()
        ctk.CTkLabel(main_area, text="Your Goals", font=("Arial", 18, "bold")).pack(pady=10)

        goals = get_goals(user_id)
        for goal in goals:
            goal_text = f"{goal[2]} (Due: {goal[4]}) - {goal[3]}"
            ctk.CTkLabel(main_area, text=goal_text).pack(anchor="w", padx=20)

        goal_entry = ctk.CTkEntry(main_area, placeholder_text="Goal Title")
        goal_entry.pack(pady=5)

        desc_entry = ctk.CTkEntry(main_area, placeholder_text="Description")
        desc_entry.pack(pady=5)

        due_entry = ctk.CTkEntry(main_area, placeholder_text="Due Date (YYYY-MM-DD)")
        due_entry.pack(pady=5)

        def save_goal():
            g, d, due = goal_entry.get(), desc_entry.get(), due_entry.get()
            if g and d and due:
                add_goal(user_id, g, d, due)
                goal_planner()

        ctk.CTkButton(main_area, text="Add Goal", command=save_goal, fg_color="#F4511E", text_color="white").pack(pady=10)

    def habit_builder():
        clear_main_area()
        ctk.CTkLabel(main_area, text="Your Habits", font=("Arial", 18, "bold")).pack(pady=10)

        habits = get_habits(user_id)
        for habit in habits:
            habit_text = f"{habit[2]} - {habit[1]}"
            ctk.CTkLabel(main_area, text=habit_text).pack(anchor="w", padx=20)

        name_entry = ctk.CTkEntry(main_area, placeholder_text="Habit Name")
        name_entry.pack(pady=5)

        desc_entry = ctk.CTkEntry(main_area, placeholder_text="Description")
        desc_entry.pack(pady=5)

        def save_habit():
            name, desc = name_entry.get(), desc_entry.get()
            if name and desc:
                add_habit(desc, name, user_id)
                habit_builder()

        ctk.CTkButton(main_area, text="Add Habit", command=save_habit, fg_color="#F4511E", text_color="white").pack(pady=10)

    def pomodoro_timer():
        clear_main_area()
        PomodoroApp(master=main_area, user_id=user_id)

    # Sidebar buttons
    for txt, cmd in [("Home", go_to_home), ("Goal Planner", goal_planner), ("Habit Builder", habit_builder), ("Pomodoro Timer", pomodoro_timer)]:
        ctk.CTkButton(sidebar, text=txt, command=cmd, fg_color="#F4511E", hover_color="#D84315",
                      text_color="white", font=("Arial", 14)).pack(pady=10, fill="x", padx=10)

    go_to_home()  # Default view

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
