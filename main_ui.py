import customtkinter as ctk
from pomodorocoding import PomodoroApp
from models import add_user, get_users, add_goal, get_goals, add_habit, get_habits, add_timers, timers, user_exists, save_timer_mode, load_timer_modes
from argon2 import PasswordHasher
from tkinter import messagebox
from datetime import datetime
import sqlite3

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

# ----------------------------------------------------------------CODE UNTUK LOGIN-----------------------------------------------------------------
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

# ----------------------------------------------------------------CODE UNTUK REGISTER----------------------------------------------------------------
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

# ----------------------------------------------------------------CODE UNTUK MAIN PAGE----------------------------------------------------------------

def show_main(user_id):
    for widget in app.winfo_children():
        widget.destroy()

    header = ctk.CTkFrame(app, height=60, fg_color="#FF5722")
    header.pack(fill="x")

    hamburger_btn = ctk.CTkButton(header, text="☰", width=50, command=lambda: toggle_sidebar(), fg_color="white", text_color="black")
    hamburger_btn.pack(side="left", padx=10, pady=10)

    title = ctk.CTkLabel(header, text="IMPROVE - MAKE LIFE BETTER", font=ctk.CTkFont(size=20, weight="bold"), text_color="white", fg_color="#FF5722")
    title.pack(pady=10)

    wrapper = ctk.CTkFrame(app)
    wrapper.pack(fill="both", expand=True)

    sidebar = ctk.CTkFrame(wrapper, width=0, fg_color="#FF5722")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    main_area = ctk.CTkFrame(wrapper, fg_color="white")
    main_area.pack(side="right", fill="both", expand=True)
    main_area = main_area

    ctk.CTkButton(sidebar, text="Home Page", command=lambda: go_to_home(main_area),
              fg_color="#F4511E", text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Goal Planner", command=lambda: goal_planner(main_area),
              fg_color="#F4511E", text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Habit Builder", command=lambda: habit_builder_page(main_area, user_id),
              fg_color="#F4511E", text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Pomodoro Timer", command=lambda: pomodoro_timer_page(main_area, user_id),
              fg_color="#F4511E", text_color="white").pack(pady=10, fill="x", padx=10)

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

    def go_to_home(main_area):
        clear_main_area()
        ctk.CTkLabel(main_area, text="Home Page", font=("Arial", 18, "bold")).pack(pady=10)
    
    def goal_planner(main_area):
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

        ctk.CTkButton(main_area, text="Add Goal", command=lambda: [add_goal(user_id, goal_entry.get(), desc_entry.get(), due_entry.get()), goal_planner(main_area)], fg_color="#F4511E", text_color="white").pack(pady=10)
    
    def habit_builder_page(main_content, user_id):
        for widget in main_content.winfo_children():
            widget.destroy()

        # Load habits from the database
        raw_habits = get_habits(user_id)

        # Transform habits into the format used by the UI
        habits = []
        for habit in raw_habits:
            habits.append({
                "title": habit[2],  # habit_name
                "description": habit[1],  # description
                "days": {day: False for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
            })

        def draw_habits():
            for widget in habit_list_frame.winfo_children():
                widget.destroy()

            for habit in habits:
                habit_card = ctk.CTkFrame(habit_list_frame, fg_color="#d9d9d9", corner_radius=10)
                habit_card.pack(anchor="nw", padx=20, pady=10, fill="x")

                habit_title = ctk.CTkLabel(habit_card, text=habit["title"], font=ctk.CTkFont(size=45), text_color="black")
                habit_title.pack(anchor="nw", padx=10, pady=(10, 0))

                habit_subtext = ctk.CTkLabel(habit_card, text=habit["description"], font=ctk.CTkFont(size=30), text_color="black")
                habit_subtext.pack(anchor="nw", padx=10, pady=(0, 10))

                days_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
                days_frame.pack(anchor="nw", padx=10, pady=10)
                for day in habit["days"]:
                    ctk.CTkLabel(days_frame, text=day, text_color="black", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)

                circle_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
                circle_frame.pack(anchor="nw", padx=10, pady=(0, 10))

                def make_toggle_func(habit, day):
                    def toggle():
                        habit["days"][day] = not habit["days"][day]
                        draw_habits()
                    return toggle

                for day in habit["days"]:
                    color = "#7d6b6b" if habit["days"][day] else "#d1b5b5"
                    ctk.CTkButton(circle_frame, text="", width=30, height=30, corner_radius=15, fg_color=color,
                                hover=False, command=make_toggle_func(habit, day)).pack(side="left", padx=10)

        def open_add_habit_popup():
            popup = ctk.CTkToplevel()
            popup.title("Add New Habit")
            popup.geometry("600x500")
            popup.attributes('-topmost', True)

            title_entry = ctk.CTkEntry(popup, placeholder_text="Habit Title")
            title_entry.pack(pady=10)
            desc_entry = ctk.CTkEntry(popup, placeholder_text="Habit Description")
            desc_entry.pack(pady=10)

            def save_habit():
                title = title_entry.get().strip()
                desc = desc_entry.get().strip() or "No description"
                if title:
                    add_habit(desc, title, user_id)  # Save to DB
                    habits.append({
                        "title": title,
                        "description": desc,
                        "days": {day: False for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
                    })
                    draw_habits()
                    popup.destroy()

            ctk.CTkButton(popup, text="Add Habit", command=save_habit).pack(pady=20)

        title = ctk.CTkLabel(main_content, text="Habit builder", font=ctk.CTkFont(size=95, weight="bold"), text_color="black")
        title.pack(anchor="nw", padx=20, pady=(20, 10))

        create_btn = ctk.CTkButton(main_content, text="Create new habit +", fg_color="#d9d9d9", text_color="black",
                                    hover_color="#cccccc", command=open_add_habit_popup)
        create_btn.pack(anchor="nw", padx=20, pady=(0, 20))

        habit_list_frame = ctk.CTkFrame(main_content, fg_color="white")
        habit_list_frame.pack(fill="both", expand=True)

        draw_habits()

    def pomodoro_timer_page(main_content, user_id):
        for widget in main_content.winfo_children():
            widget.destroy()

        # Load saved modes from DB and merge with defaults
        saved_modes = load_timer_modes(user_id)
        timer_modes = {
            "Pomodoro": [("Work", 25 * 60), ("Break", 5 * 60)]
        }
        timer_modes.update(saved_modes)  # Add custom modes from DB to the default ones

        current_mode = ["Pomodoro"]
        sessions = timer_modes[current_mode[0]]
        session_index = [0]
        time_left = [sessions[session_index[0]][1]]
        running = [False]
        session_counter = [0]
        session_start = [None]

        def _format_time(seconds):
            m, s = divmod(seconds, 60)
            return f"{m:02d}:{s:02d}"

        def _update_session_label():
            name = sessions[session_index[0]][0]
            session_label.configure(text="Work Session" if name in ["Work", "Focus"] else "Break Time",
                                    text_color="#2E86C1" if name in ["Work", "Focus"] else "#27AE60")

        def _switch_session():
            prev_session_name = sessions[session_index[0]][0]
            end_time = int(datetime.now().timestamp())
            if prev_session_name in ["Work", "Focus"]:
                start_time_val = session_start[0] if session_start[0] else end_time
                duration = end_time - start_time_val
                completed = 1
                task = current_mode[0] + " - " + prev_session_name
                try:
                    add_timers(task, start_time_val, end_time, duration, completed, user_id)
                    print(f"Session saved: {task}, {start_time_val}, {end_time}, {duration}, {user_id}")
                except Exception as e:
                    print("Error saving timer:", e)

            session_index[0] = (session_index[0] + 1) % len(sessions)
            time_left[0] = sessions[session_index[0]][1]

            _update_session_label()
            timer_label.configure(text=_format_time(time_left[0]))
            status_label.configure(text=f"{sessions[session_index[0]][0]} starting...")

            if sessions[session_index[0]][0] in ["Work", "Focus"]:
                session_start[0] = int(datetime.now().timestamp())
            else:
                session_start[0] = None

        def _countdown():
            if running[0] and time_left[0] > 0:
                time_left[0] -= 1
                timer_label.configure(text=_format_time(time_left[0]))
                main_content.after(1000, _countdown)
            elif running[0]:
                running[0] = False
                status_label.configure(text="Session Complete!")
                _switch_session()

        def start_timer():
            if not running[0]:
                running[0] = True
                session_type = sessions[session_index[0]][0]
                if session_type in ["Work", "Focus"]:
                    session_start[0] = int(datetime.now().timestamp())
                status_label.configure(text="Running...")
                _countdown()

        def reset_timer():
            running[0] = False
            time_left[0] = sessions[session_index[0]][1]
            timer_label.configure(text=_format_time(time_left[0]))
            status_label.configure(text="Reset")
            _update_session_label()

        def switch_mode(new_mode):
            nonlocal sessions
            running[0] = False
            current_mode[0] = new_mode
            sessions = timer_modes[new_mode]
            session_index[0] = 0
            session_counter[0] = 0
            time_left[0] = sessions[0][1]
            counter_label.configure(text=f"Sessions Completed: {session_counter[0]}")
            _update_session_label()
            timer_label.configure(text=_format_time(time_left[0]))
            status_label.configure(text=f"{new_mode} Mode Selected")
            session_start[0] = None

        def add_custom_timer():
            popup = ctk.CTkToplevel()
            popup.title("Add Custom Timer")
            popup.geometry("400x300")
            popup.attributes('-topmost', True)

            name_entry = ctk.CTkEntry(popup, placeholder_text="Mode Name")
            name_entry.pack(pady=10)
            focus_entry = ctk.CTkEntry(popup, placeholder_text="Focus Minutes (int)")
            focus_entry.pack(pady=10)
            rest_entry = ctk.CTkEntry(popup, placeholder_text="Rest Minutes (int)")
            rest_entry.pack(pady=10)

            def save_custom():
                try:
                    name = name_entry.get().strip()
                    focus_min = int(focus_entry.get().strip())
                    rest_min = int(rest_entry.get().strip())
                    if name and focus_min > 0 and rest_min > 0:
                        # Save to DB
                        save_timer_mode(name, focus_min * 60, rest_min * 60, user_id)
                        # Update in-memory dict & UI
                        timer_modes[name] = [("Focus", focus_min * 60), ("Rest", rest_min * 60)]
                        mode_options.append(name)
                        mode_menu.configure(values=mode_options)
                        popup.destroy()
                    else:
                        messagebox.showerror("Error", "Please enter valid values!")
                except ValueError:
                    messagebox.showerror("Error", "Minutes must be integers!")

            ctk.CTkButton(popup, text="Save Timer", command=save_custom).pack(pady=20)

        top_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        top_frame.pack(anchor="nw", padx=20, pady=10)

        ctk.CTkLabel(top_frame, text="Mode:", font=("Inter", 18, "bold")).pack(side="left", padx=(0, 5))

        mode_options = list(timer_modes.keys())
        mode_menu = ctk.CTkOptionMenu(top_frame, values=mode_options, command=switch_mode)
        mode_menu.pack(side="left", padx=5)

        ctk.CTkButton(top_frame, text="+ Add Custom Timer", command=add_custom_timer,
                    fg_color="#A3A1A1", hover_color="#8F8D8D", text_color="white").pack(side="left", padx=10)

        timer_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        timer_frame.pack(expand=True, fill="both")

        session_label = ctk.CTkLabel(timer_frame, text="Work Session", font=("Inter", 95, "bold"), text_color="#2E86C1")
        session_label.pack(pady=30)

        timer_label = ctk.CTkLabel(timer_frame, text=_format_time(time_left[0]), font=("Inter", 200), text_color="#A3A1A1")
        timer_label.pack(pady=20)

        counter_label = ctk.CTkLabel(timer_frame, text=f"Sessions Completed: {session_counter[0]}", font=("Inter", 24), text_color="#555555")
        counter_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(timer_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Start", width=300, height=100, font=("Inter", 30, "bold"), fg_color="#A3A1A1",
                    hover_color="#8F8D8D", text_color="white", command=start_timer).pack(side="left", padx=20)

        ctk.CTkButton(btn_frame, text="Reset", width=300, height=100, font=("Inter", 30, "bold"), fg_color="#A3A1A1",
                    hover_color="#8F8D8D", text_color="white", command=reset_timer).pack(side="left", padx=20)

        status_label = ctk.CTkLabel(timer_frame, text="Ready", font=("Inter", 20), text_color="#888888")
        status_label.pack(pady=10)

        _update_session_label()

    def goal_planner_page(master, color, placeholder):
        goal_frame = ctk.CTkFrame(master, fg_color="#d3d3d3")
        goal_frame.pack(fill="x", pady=10)

        # Goal input
        goal_entry_frame = ctk.CTkFrame(goal_frame, fg_color=color)
        goal_entry_frame.pack(fill="x")

        goal_entry_label = ctk.CTkLabel(goal_entry_frame, text="Goal:", font=("Arial", 18, "bold"), text_color="black")
        goal_entry_label.pack(side="left", padx=10)

        goal_input = ctk.CTkEntry(goal_entry_frame, placeholder_text=placeholder)
        goal_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Headers
        header_frame = ctk.CTkFrame(goal_frame, fg_color="#d3d3d3")
        header_frame.pack(fill="x")

        step_label = ctk.CTkLabel(header_frame, text="Step to take", font=("Arial", 14, "bold"))
        step_label.pack(side="left", fill="x", expand=True)

        deadline_label = ctk.CTkLabel(header_frame, text="Deadline", font=("Arial", 14, "bold"), anchor="e")
        deadline_label.pack(side="right", fill="x", expand=True)

        # Rows for steps
        for _ in range(3):
            row = ctk.CTkFrame(goal_frame, fg_color="#d3d3d3")
            row.pack(fill="x", pady=2)
            step_entry = ctk.CTkEntry(row, placeholder_text="Enter step")
            step_entry.pack(side="left", fill="x", expand=True, padx=5)
            deadline_entry = ctk.CTkEntry(row, placeholder_text="Deadline")
            deadline_entry.pack(side="right", fill="x", expand=True, padx=5)

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
