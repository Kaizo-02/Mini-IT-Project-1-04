import customtkinter as ctk
import tkinter as tk
from tkinter import colorchooser
# from pomodorocoding import PomodoroApp # Assuming this is available and compatible
from models import add_user, get_users, add_goal, get_goals, add_habit, get_habits, add_timers, user_exists, save_timer_mode, load_timer_modes, load_user_settings, save_user_settings
from argon2 import PasswordHasher
from tkinter import messagebox
from datetime import datetime
import sqlite3
from tkinter import filedialog
from PIL import Image, ImageTk


ph = PasswordHasher()

e1, e2, e3 = None, None, None
app = None

# Using a class to manage global settings and provide a 'controller'
class AppSettings:
    def __init__(self):
        self.background_color = "#d3d3d3"
        self.font_family = "Inter"
        self.font_size = 12

controller = AppSettings() # Initialize the controller

def logout():
    # Clear the main window to logout the user
    for widget in app.winfo_children():
        widget.destroy()

    # Show the login screen again to allow the user to switch accounts
    show_login()

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

def save_user_settings(user_id, background_color, font_family, font_size, background_image_path=None):
    """
    Placeholder function to save user settings.
    In a real app, this would interact with a database or config file.
    'background_image_path' is an optional argument.
    """
    print(f"Saving settings for user {user_id}:")
    print(f"  Background Color: {background_color}")
    print(f"  Font Family: {font_family}")
    print(f"  Font Size: {font_size}")
    if background_image_path:
        print(f"  Background Image Path: {background_image_path}")
    # Here, you would add your actual code to save these settings
    # to a database, a JSON file, or another persistent storage.

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
                messagebox.showerror("Login Failed", "Incorrect username or password.")
                return
    messagebox.showerror("Login Failed", "User not found.")

def save_user():
    username = e1.get()
    email = e3.get()
    password = e2.get()

    if not username or username == "Choose a Username":
        messagebox.showerror("Registration Error", "Please enter a username.")
        return
    if not email or email == "Your Email":
        messagebox.showerror("Registration Error", "Please enter your email.")
        return
    if not password or password == "Choose a Password":
        messagebox.showerror("Registration Error", "Please enter a password.")
        return

    if user_exists(username): # Assuming user_exists checks by username
        messagebox.showerror("Registration Error", "Username already exists. Please choose a different one.")
        return

    try:
        hashed_password = ph.hash(password)
        add_user(username, email, hashed_password)
        print("User registered successfully!")
        messagebox.showinfo("Registration Success", "User registered successfully! You can now log in.")
        show_login()
    except Exception as e:
        print(f"Error during registration: {e}")
        messagebox.showerror("Registration Error", f"An error occurred during registration: {e}")


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
    global app
    for widget in app.winfo_children():
        widget.destroy()

    # Load settings from the database
    background_color, font_family, font_size = load_user_settings(user_id)
    controller.background_color = background_color if background_color else "#d3d3d3"
    controller.font_family = font_family if font_family else "Inter"
    controller.font_size = font_size if font_size else 12

    # Create a wrapper to hold header, sidebar, and main_area
    wrapper = ctk.CTkFrame(app)
    wrapper.pack(fill="both", expand=True)

    # Header with the background color applied
    header = ctk.CTkFrame(wrapper, height=60, fg_color=controller.background_color)  # Apply background color to header
    header.pack(fill="x")

    # Function to logout the user (clear main window and show the login screen)
    def logout():
        # Clear the main window to logout the user
        for widget in app.winfo_children():
            widget.destroy()

        # Show the login screen again to allow the user to switch accounts
        show_login()

    # Function to switch the account (logout and show login screen)
    def switch_account():
        logout()

    def toggle_menu():
        if hasattr(toggle_menu, "menu") and toggle_menu.menu.winfo_exists():
            if toggle_menu.menu.winfo_ismapped():
                toggle_menu.menu.place_forget()
            else:
                toggle_menu.menu.place(x=850, y=55)  # adjust as needed
        else:
            show_menu()

    def show_menu():
        menu = ctk.CTkFrame(app, fg_color="white", width=150, height=100, corner_radius=10)
        menu.place(x=850, y=55)

        ctk.CTkButton(menu, text="Logout", command=logout, fg_color="transparent", text_color="black").pack(pady=5)
        ctk.CTkButton(menu, text="Switch Account", command=switch_account, fg_color="transparent", text_color="black").pack(pady=5)

        toggle_menu.menu = menu  # store menu so we can toggle it

    # Profile Button
    profile_btn = ctk.CTkButton(
        header, text="👤", width=40, height=40,
        fg_color="gray", text_color="white", command=toggle_menu
    )
    profile_btn.pack(side="right", padx=10, pady=10)

    # Hamburger button and title in header
    hamburger_btn = ctk.CTkButton(header, text="☰", width=50, command=lambda: toggle_sidebar(), fg_color="white", text_color="black")
    hamburger_btn.pack(side="left", padx=10, pady=10)

    # Title with background color applied to title frame
    title_frame = ctk.CTkFrame(header, fg_color=controller.background_color)  # Frame around the title (changes background)
    title_frame.pack(side="left", padx=10, pady=10)

    title = ctk.CTkLabel(title_frame, text="IMPROVE - MAKE LIFE BETTER", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")  # Apply color to title label
    title.pack(pady=10, padx=10)

    # Sidebar with background color applied
    sidebar = ctk.CTkFrame(wrapper, width=200, fg_color=controller.background_color)  # Apply background color to sidebar
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)  # Prevent sidebar from resizing itself

    # Add sidebar buttons with the same background color
    ctk.CTkButton(sidebar, text="Home Page", command=lambda: go_to_home(main_area), fg_color=controller.background_color, text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Goal Planner", command=lambda: goal_planner(main_area, user_id), fg_color=controller.background_color, text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Habit Builder", command=lambda: habit_builder_page(main_area, user_id), fg_color=controller.background_color, text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Pomodoro Timer", command=lambda: pomodoro_timer_page(main_area, user_id, controller), fg_color=controller.background_color, text_color="white").pack(pady=10, fill="x", padx=10)
    ctk.CTkButton(sidebar, text="Settings", command=lambda: settings_page(main_area, user_id, header, title, sidebar, title_frame), fg_color=controller.background_color, text_color="white").pack(pady=10, fill="x", padx=10)

    # Main content area (right section)
    main_area = ctk.CTkFrame(wrapper, fg_color="white")
    main_area.pack(side="right", fill="both", expand=True)

    # Function to toggle the sidebar visibility
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

    # Function to clear main area when switching pages
    def clear_main_area():
        for widget in main_area.winfo_children():
            widget.destroy()

    # Function to show the home page
    def go_to_home(main_area):
        clear_main_area()
        ctk.CTkLabel(main_area, text="Home Page", font=(controller.font_family, controller.font_size + 28), text_color="black").pack(pady=10)

    go_to_home(main_area)

    def logout():
        # Clear the main window to logout the user
        for widget in app.winfo_children():
            widget.destroy()

        # Show the login screen again to allow the user to switch accounts
        show_login()

    def switch_account():
        # Allow the user to switch to another account (logout and show login screen)
        logout()

    def goal_planner(main_area, user_id):
        clear_main_area() # Clear the main area before drawing the new content

        # Frame to hold the goal list
        goal_list_frame = ctk.CTkScrollableFrame(main_area, fg_color="white")
        goal_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(goal_list_frame, text="Your Goals", font=(controller.font_family, controller.font_size + 28), text_color="black").pack(pady=10)

        # Fetch goals from the database and display them
        def display_goals():
            # Clear existing goals in the display area to avoid duplicates, except the title
            for widget in goal_list_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Your Goals" in widget.cget("text"):
                    continue # Keep the title label
                widget.destroy()
            
            # Re-add the title if it was removed by mistake (defensive)
            if not any(isinstance(w, ctk.CTkLabel) and "Your Goals" in w.cget("text") for w in goal_list_frame.winfo_children()):
                ctk.CTkLabel(goal_list_frame, text="Your Goals", font=(controller.font_family, controller.font_size + 28), text_color="black").pack(pady=10)


            goals = get_goals(user_id)  # Fetch goals from the database
            if not goals:
                ctk.CTkLabel(goal_list_frame, text="No goals added yet.", font=(controller.font_family, controller.font_size), text_color="gray").pack(pady=10)
            else:
                for goal in goals:
                    # Create a frame for each goal for better organization
                    goal_card = ctk.CTkFrame(goal_list_frame, fg_color="#d9d9d9", corner_radius=10)
                    goal_card.pack(fill="x", pady=5, padx=10)

                    goal_title_label = ctk.CTkLabel(goal_card, text=f"Goal: {goal[2]}", font=(controller.font_family, controller.font_size + 4), text_color="black")
                    goal_title_label.pack(anchor="w", padx=10, pady=(5,0))

                    goal_desc_label = ctk.CTkLabel(goal_card, text=f"Description: {goal[3]}", font=(controller.font_family, controller.font_size), text_color="black")
                    goal_desc_label.pack(anchor="w", padx=10)

                    goal_due_label = ctk.CTkLabel(goal_card, text=f"Due Date: {goal[4]}", font=(controller.font_family, controller.font_size), text_color="black")
                    goal_due_label.pack(anchor="w", padx=10, pady=(0,5))


        # Input fields for saving a new goal
        input_frame = ctk.CTkFrame(main_area, fg_color="transparent")
        input_frame.pack(pady=20, padx=20, fill="x")

        goal_entry = ctk.CTkEntry(input_frame, placeholder_text="Goal Title", font=(controller.font_family, controller.font_size))
        goal_entry.pack(pady=5, fill="x")

        desc_entry = ctk.CTkEntry(input_frame, placeholder_text="Description", font=(controller.font_family, controller.font_size))
        desc_entry.pack(pady=5, fill="x")

        due_entry = ctk.CTkEntry(input_frame, placeholder_text="Due Date (YYYY-MM-DD)", font=(controller.font_family, controller.font_size))
        due_entry.pack(pady=5, fill="x")

        # Save new goal to the database
        def save_goal():
            g, d, due = goal_entry.get().strip(), desc_entry.get().strip(), due_entry.get().strip()
            if g and d and due:
                # Basic date format validation (YYYY-MM-DD)
                try:
                    datetime.strptime(due, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Invalid Date", "Due Date must be in YYYY-MM-DD format.")
                    return

                # Save the goal to the database
                add_goal(user_id, g, d, due)
                messagebox.showinfo("Goal Added", "Your goal has been added successfully!")
                
                # Clear input fields
                goal_entry.delete(0, ctk.END)
                desc_entry.delete(0, ctk.END)
                due_entry.delete(0, ctk.END)
                
                display_goals()  # Refresh the goal list immediately
            else:
                messagebox.showerror("Input Error", "Please fill in all fields: Goal Title, Description, and Due Date.")

        ctk.CTkButton(input_frame, text="Add Goal", command=save_goal,
                         fg_color="#F4511E", text_color="white", font=(controller.font_family, controller.font_size, "bold")).pack(pady=10)

        display_goals()  # Initially show goals after setting up the UI

#--------------------------------------------------------------HABIT BUILDER PAGE-------------------------------------------------------------
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

            if not habits:
                ctk.CTkLabel(habit_list_frame, text="No habits added yet.", font=(controller.font_family, controller.font_size), text_color="gray").pack(pady=20)
                return

            for habit in habits:
                habit_card = ctk.CTkFrame(habit_list_frame, fg_color="#d9d9d9", corner_radius=10)
                habit_card.pack(anchor="nw", padx=20, pady=10, fill="x")

                habit_title = ctk.CTkLabel(habit_card, text=habit["title"], font=ctk.CTkFont(family=controller.font_family, size=controller.font_size + 30), text_color="black")
                habit_title.pack(anchor="nw", padx=10, pady=(10, 0))

                habit_subtext = ctk.CTkLabel(habit_card, text=habit["description"], font=ctk.CTkFont(family=controller.font_family, size=controller.font_size + 18), text_color="black")
                habit_subtext.pack(anchor="nw", padx=10, pady=(0, 10))

                days_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
                days_frame.pack(anchor="nw", padx=10, pady=10)
                for day in habit["days"]:
                    ctk.CTkLabel(days_frame, text=day, text_color="black", font=ctk.CTkFont(family=controller.font_family, size=controller.font_size)).pack(side="left", padx=10)

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

            title_entry = ctk.CTkEntry(popup, placeholder_text="Habit Title", font=(controller.font_family, controller.font_size))
            title_entry.pack(pady=10)
            desc_entry = ctk.CTkEntry(popup, placeholder_text="Habit Description", font=(controller.font_family, controller.font_size))
            desc_entry.pack(pady=10)

            def save_habit():
                title = title_entry.get().strip()
                desc = desc_entry.get().strip() or "No description"
                if title:
                    add_habit(desc, title, user_id)  # Save to DB
                    # Refresh raw_habits from DB to get the latest data, including new habit ID
                    habits.append({
                        "title": title,
                        "description": desc,
                        "days": {day: False for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
                    })
                    draw_habits()
                    popup.destroy()
                else:
                    messagebox.showerror("Error", "Habit title cannot be empty.")


            ctk.CTkButton(popup, text="Add Habit", command=save_habit, font=(controller.font_family, controller.font_size, "bold")).pack(pady=20)

        title = ctk.CTkLabel(main_content, text="Habit builder", font=ctk.CTkFont(family=controller.font_family, size=controller.font_size + 83, weight="bold"), text_color="black")
        title.pack(anchor="nw", padx=20, pady=(20, 10))

        create_btn = ctk.CTkButton(main_content, text="Create new habit +", fg_color="#d9d9d9", text_color="black",
                                     hover_color="#cccccc", command=open_add_habit_popup, font=(controller.font_family, controller.font_size, "bold"))
        create_btn.pack(anchor="nw", padx=20, pady=(0, 20))

        habit_list_frame = ctk.CTkScrollableFrame(main_content, fg_color="white") # Use scrollable frame for habits
        habit_list_frame.pack(fill="both", expand=True)

        draw_habits()

        #_-------------------------------------------------------------POMODORO TIMER PAGE------------------------------------------------------------_

    def pomodoro_timer_page(main_content, user_id, controller):
        for widget in main_content.winfo_children():
            widget.destroy()
        custom_font = ctk.CTkFont(family=controller.font_family, size=controller.font_size)


        # Load saved modes from DB and merge with defaults
        saved_modes = load_timer_modes(user_id)
        timer_modes = {
            "Pomodoro": [("Work", 25 * 60), ("Break", 5 * 60)],
            "Valorant": [("Headshots!", 45 * 60), ("Chill for a bit", 5 * 60)],
            "Testing": [("Customise this", 1 * 5), ("Break up", 1 * 5)]

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
                                     text_color="#2E86C1" if name in ["Work", "Focus"] else "#27AE60",
                                     font=custom_font) # Apply custom font here

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

            name_entry = ctk.CTkEntry(popup, placeholder_text="Mode Name", font=(controller.font_family, controller.font_size))
            name_entry.pack(pady=10)
            focus_entry = ctk.CTkEntry(popup, placeholder_text="Focus Minutes (int)", font=(controller.font_family, controller.font_size))
            focus_entry.pack(pady=10)
            rest_entry = ctk.CTkEntry(popup, placeholder_text="Rest Minutes (int)", font=(controller.font_family, controller.font_size))
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
                        messagebox.showerror("Error", "Please enter valid values for name, focus, and rest minutes!")
                except ValueError:
                    messagebox.showerror("Error", "Minutes must be integers!")

            ctk.CTkButton(popup, text="Save Timer", command=save_custom, font=(controller.font_family, controller.font_size, "bold")).pack(pady=20)

        top_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        top_frame.pack(anchor="nw", padx=20, pady=10)

        ctk.CTkLabel(top_frame, text="Mode:", font=custom_font).pack(side="left", padx=(0, 5))

        mode_options = list(timer_modes.keys())
        mode_menu = ctk.CTkOptionMenu(top_frame, values=mode_options, command=switch_mode, font=custom_font)
        mode_menu.pack(side="left", padx=5)

        ctk.CTkButton(top_frame, text="+ Add Custom Timer", command=add_custom_timer,
                         fg_color="#A3A1A1", hover_color="#8F8D8D", text_color="white", font=custom_font).pack(side="left", padx=10)

        timer_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        timer_frame.pack(expand=True, fill="both")

        session_label = ctk.CTkLabel(timer_frame, text="Work Session", font=custom_font, text_color="#2E86C1")
        session_label.pack(pady=30)

        timer_label = ctk.CTkLabel(timer_frame, text=_format_time(time_left[0]), font=ctk.CTkFont(family=controller.font_family, size=controller.font_size + 100)) # Larger font for timer
        timer_label.pack(pady=20)

        counter_label = ctk.CTkLabel(timer_frame, text=f"Sessions Completed: {session_counter[0]}", font=custom_font)
        counter_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(timer_frame, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="Start", width=300, height=100, font=custom_font, fg_color="#A3A1A1",
                         hover_color="#8F8D8D", text_color="white", command=start_timer).pack(side="left", padx=20)

        ctk.CTkButton(btn_frame, text="Reset", width=300, height=100, font=custom_font, fg_color="#A3A1A1",
                         hover_color="#8F8D8D", text_color="white", command=reset_timer).pack(side="left", padx=20)

        status_label = ctk.CTkLabel(timer_frame, text="Ready", font=custom_font, text_color="#888888")
        status_label.pack(pady=10)

        _update_session_label()

#--------------------------------------------------------------GOAL PLANNER PAGE (Removed the separate create_goal_section)-------------------------------------------------------------
    # This goal_planner_page was a duplicate and conflicting with the goal_planner function
    # It has been commented out to avoid confusion and ensure a single, working goal planner.
    # def goal_planner_page(master, color, placeholder, controller):
    #     custom_font = ctk.CTkFont(family=controller.font_family, size=controller.font_size)
    #     goal_frame = ctk.CTkFrame(master, fg_color="#d3d3d3")
    #     goal_frame.pack(fill="x", pady=10)

    #     # Goal input
    #     goal_entry_frame = ctk.CTkFrame(goal_frame, fg_color=color)
    #     goal_entry_frame.pack(fill="x")

    #     goal_entry_label = ctk.CTkLabel(goal_entry_frame, text="Goal:", font=custom_font, text_color="black")
    #     goal_entry_label.pack(side="left", padx=10)

    #     goal_input = ctk.CTkEntry(goal_entry_frame, placeholder_text=placeholder, font=custom_font)
    #     goal_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)

    #     # Headers
    #     header_frame = ctk.CTkFrame(goal_frame, fg_color="#d3d3d3")
    #     header_frame.pack(fill="x")

    #     step_label = ctk.CTkLabel(header_frame, text="Step to take", font=custom_font)
    #     step_label.pack(side="left", fill="x", expand=True)

    #     deadline_label = ctk.CTkLabel(header_frame, text="Deadline", font=custom_font, anchor="e")
    #     deadline_label.pack(side="right", fill="x", expand=True)

    #     # Rows for steps
    #     for _ in range(3):
    #         row = ctk.CTkFrame(goal_frame, fg_color="#d3d3d3")
    #         row.pack(fill="x", pady=2)
    #         step_entry = ctk.CTkEntry(row, placeholder_text="Enter step", font=custom_font)
    #         step_entry.pack(side="left", fill="x", expand=True, padx=5)
    #         deadline_entry = ctk.CTkEntry(row, placeholder_text="Deadline", font=custom_font)
    #         deadline_entry.pack(side="right", fill="x", expand=True, padx=5)

    def choose_color(header, sidebar, title_frame):
        # Open color picker dialog and get the selected color
        color_code = colorchooser.askcolor(title="Choose Header/Sidebar Color")[1]
        if color_code:  # If a color was selected
            # Apply the selected color to the header and sidebar
            header.configure(fg_color=color_code)
            sidebar.configure(fg_color=color_code)
            title_frame.configure(fg_color=color_code) # Apply to the title_frame as well
            # Also change the color of the text box (sidebar buttons)
            for widget in sidebar.winfo_children():
                # Only reconfigure if it's a CTkButton (the sidebar buttons)
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(fg_color=color_code)

            # Update the controller's background color
            controller.background_color = color_code
            print(f"Selected color: {color_code}")
            return color_code
        return None

    def settings_page(main_area, user_id, header, title, sidebar, title_frame):
        clear_main_area()

        # Settings Page Title
        ctk.CTkLabel(main_area, text="Settings",
                    font=(controller.font_family, 60, "bold"),
                    text_color="black").pack(pady=20)

        # Background Image Option
        def choose_background_image():
            filetypes = [
                ("All image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("BMP files", "*.bmp"),
                ("GIF files", "*.gif")
                
            ]
            filepath = filedialog.askopenfilename(title="Choose Background Image", filetypes=filetypes)
            if filepath:
                try:
                    img = Image.open(filepath)

                    current_width = main_area.winfo_width()
                    current_height = main_area.winfo_height()

                    if current_width == 1 and app.winfo_width() > 1:
                        current_width = app.winfo_width()
                    if current_height == 1 and app.winfo_height() > 1:
                        current_height = app.winfo_height()

                    current_width = max(10, current_width)
                    current_height = max(10, current_height)

                    img = img.resize((current_width, current_height), Image.LANCZOS)
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(current_width, current_height))

                    controller.background_img = ctk_img

                    if not hasattr(controller, "bg_label") or not controller.bg_label or not controller.bg_label.winfo_exists():
                        controller.bg_label = ctk.CTkLabel(main_area, text="", image=ctk_img)
                        controller.bg_label.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
                        controller.bg_label.lower()
                    else:
                        controller.bg_label.configure(image=ctk_img)

                    controller.bg_label.image = ctk_img
                    controller.current_bg_image_path = filepath # Store the path in controller

                    # Call the global save_user_settings
                    save_user_settings(user_id, background_color=controller.background_color,
                                    font_family=controller.font_family, font_size=controller.font_size,
                                    background_image_path=filepath)
                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to load or apply image: {e}")

        ctk.CTkButton(main_area, text="Choose Background Image", command=choose_background_image,
                    font=(controller.font_family, controller.font_size, "bold")).pack(pady=20)

        # Background Color Option (for Header/Sidebar)
        ctk.CTkButton(main_area, text="Choose Header/Sidebar Color", command=lambda: choose_color(header, sidebar, title_frame),
                    font=(controller.font_family, controller.font_size, "bold")).pack(pady=20)

        # Font Family Option
        ctk.CTkLabel(main_area, text="Font Family:",
                    font=(controller.font_family, controller.font_size + 8),
                    text_color="#000000").pack(pady=10)
        font_family_var = ctk.StringVar(value=controller.font_family)
        font_family_selector = ctk.CTkOptionMenu(main_area, values=["Inter", "Arial", "Courier New", "Times New Roman", "Verdana", "Helvetica"],
                                                variable=font_family_var,
                                                font=(controller.font_family, controller.font_size))
        font_family_selector.pack(pady=10)

        # Font Size Option
        font_size_mapping = {
            "Small": 12,
            "Normal": 20,
            "Large": 30,
            "Extra Large": 40
        }
        reverse_mapping = {v: k for k, v in font_size_mapping.items()}
        initial_label = reverse_mapping.get(controller.font_size, "Normal")
        font_size_var = ctk.StringVar(value=initial_label)

        ctk.CTkLabel(main_area, text="Font Size:",
                    font=(controller.font_family, controller.font_size + 8),
                    text_color="#000000").pack(pady=10)
        font_size_selector = ctk.CTkOptionMenu(main_area, values=list(font_size_mapping.keys()),
                                            variable=font_size_var,
                                            font=(controller.font_family, controller.font_size))
        font_size_selector.pack(pady=10)

        # Apply Settings Button
        def apply_settings():
            new_font_family = font_family_var.get()
            new_font_size = font_size_mapping[font_size_var.get()]

            # Update controller settings
            controller.font_family = new_font_family
            controller.font_size = new_font_size

            # Apply to the 'title' label (assuming it's a CTkLabel)
            title.configure(font=ctk.CTkFont(family=new_font_family, size=new_font_size, weight="bold"))

            # Apply to sidebar buttons
            for widget in sidebar.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(font=ctk.CTkFont(family=new_font_family, size=new_font_size))

            # Re-render the current settings page to apply new fonts to its own widgets
            settings_page(main_area, user_id, header, title, sidebar, title_frame)

            # Call the global save_user_settings
            save_user_settings(user_id, background_color=controller.background_color,
                            font_family=new_font_family, font_size=new_font_size,
                            background_image_path=controller.current_bg_image_path) # Pass the stored path

            messagebox.showinfo("Settings Applied", f"Font: {new_font_family}, Size: {new_font_size}")

        ctk.CTkButton(main_area, text="Apply Settings", command=apply_settings,
                    font=(controller.font_family, controller.font_size, "bold")).pack(pady=30)
def run_app():
    global app
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("IMPROVE - MAKE LIFE BETTER")
    app.geometry("1000x700")
    app.resizable(True, True)
    show_login()
    app.mainloop()

run_app()