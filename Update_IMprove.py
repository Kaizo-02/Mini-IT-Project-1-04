import customtkinter as ctk
from tkinter import messagebox, colorchooser
from database import add_goal, get_goals, add_user, get_users, create_connection, get_habits, add_habit, load_timer_modes, add_timers, save_timer_mode , delete_goal_from_db
from tkcalendar import Calendar
from argon2 import PasswordHasher
from datetime import datetime

goals_data = []
goal_id_counter = [1]

def get_goals_func(user_id):
    return [(g["id"], g["user_id"], g["title"], g["description"], g["deadline"]) for g in goals_data if g["user_id"] == user_id]

def add_goal_func(user_id, title, description, deadline):
    goals_data.append({
        "id": goal_id_counter[0],
        "user_id": user_id,
        "title": title,
        "description": description,
        "deadline": deadline
    })
    goal_id_counter[0] += 1

def update_goal_func(goal_id, title, description, deadline):
    for g in goals_data:
        if g["id"] == goal_id:
            g["title"] = title
            g["description"] = description
            g["deadline"] = deadline
            break

def delete_goal_func(goal_id):
    global goals_data
    goals_data = [g for g in goals_data if g["id"] != goal_id]

def load_user_settings(user_id):
 return "#FF5733", "Inter", 12

def save_user_settings(user_id, background_color, font_family, font_size):
    print(f"Settings saved for user {user_id}: color={background_color}, font={font_family}, size={font_size}")

ph = PasswordHasher()

e1, e2, e3 = None, None, None
app = None

main_bg_color = ["#FF5733"]  # Set the red color for the header/sidebar
main_font_family = ["Inter"]
main_font_size = [12]

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
    global app
    for widget in app.winfo_children():
        widget.destroy()

    # Add a motivational quote section
    quote_frame = ctk.CTkFrame(app)
    quote_frame.pack(fill="x", pady=10)  # Add some padding
    
    motivational_quote = ctk.CTkLabel(quote_frame, 
                                      text="“Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.”", 
                                      font=("Arial", 18, "italic"), text_color="black")
    motivational_quote.pack(pady=10, padx=20)

    # Load settings from the database
    background_color, font_family, font_size = load_user_settings(user_id)

    # Create a wrapper to hold header, sidebar, and main_area
    wrapper = ctk.CTkFrame(app)
    wrapper.pack(fill="both", expand=True)

    # Header with the background color applied
    header = ctk.CTkFrame(wrapper, height=60, fg_color="#FF5733")  # Apply red background to header
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
    title_frame = ctk.CTkFrame(header, fg_color="#FF5733")  # Apply red background to title frame
    title_frame.pack(side="left", padx=10, pady=10)

    title = ctk.CTkLabel(title_frame, text="IMPROVE - MAKE LIFE BETTER", font=ctk.CTkFont(size=20, weight="bold"), text_color="white")  # Apply color to title label
    title.pack(pady=10, padx=10)

    # Sidebar with background color applied
    sidebar = ctk.CTkFrame(wrapper, width=200, fg_color="#FF5733")  # Apply red background to sidebar
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)  # Prevent sidebar from resizing itself

    # Add sidebar buttons with the same background color and hover effect
    def on_button_hover(event, button):
        button.configure(fg_color="#FF6F60")  # Darken button on hover

    def on_button_leave(event, button):
        button.configure(fg_color="#FF5733")  # Reset color when hover leaves

    buttons = [
        ("Home Page", lambda: create_homepage(main_area, user_id)),
        ("Goal Planner", lambda: goal_planner(main_area, user_id, get_goals_func, add_goal_func, update_goal_func, delete_goal_func)),
        ("Habit Builder", lambda: habit_builder_page(main_area, user_id)),
        ("Pomodoro Timer", lambda: pomodoro_timer_page(main_area, user_id)),
        ("Settings", lambda: settings_page(main_area, user_id, header, title, sidebar, title_frame)),
    ]

    for text, command in buttons:
        button = ctk.CTkButton(sidebar, text=text, command=command, fg_color="#FF5733", text_color="Black", width=180)
        button.pack(pady=5, fill="x", padx=10)
        button.bind("<Enter>", lambda e, btn=button: on_button_hover(e, btn))  # Hover effect
        button.bind("<Leave>", lambda e, btn=button: on_button_leave(e, btn))  # Hover effect reset

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

def create_homepage(main_area, user_id):
    for widget in main_area.winfo_children():
        widget.destroy()

    welcome_label = ctk.CTkLabel(main_area, text=f"Welcome back, User {user_id}!", font=ctk.CTkFont(size=28, weight="bold"))
    welcome_label.pack(pady=(30,10))

    quote_text = "“Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.”"
    quote_label = ctk.CTkLabel(main_area, text=quote_text, font=ctk.CTkFont(size=18, slant="italic"), text_color="#555", wraplength=700, justify="center")
    quote_label.pack(pady=(0,30), padx=50)

    summary_frame = ctk.CTkFrame(main_area)
    summary_frame.pack(pady=10, padx=30, fill="x")

    goals_count = len(get_goals_func(user_id))
    habits_count = 4
    pomodoro_sessions = 2

    # Create summary frame to hold cards
    summary_frame = ctk.CTkFrame(main_area, fg_color="#2d1f1f", corner_radius=25)
    summary_frame.pack(pady=30, padx=50, fill="x")

    # Example usage with your data
    create_stat_card(summary_frame, "Active Goals", goals_count)
    create_stat_card(summary_frame, "Habits Tracked", habits_count)
    create_stat_card(summary_frame, "Pomodoro Sessions", pomodoro_sessions)

def create_stat_card(parent, title, value):
    # Create a frame with a subtle gradient effect (using 2 layered frames)
    outer_frame = ctk.CTkFrame(parent, corner_radius=20, fg_color=None)
    outer_frame.pack(side="left", padx=25, pady=15)

    card = ctk.CTkFrame(outer_frame, width=220, height=120, corner_radius=20, fg_color="#FF5733", border_width=2, border_color="#d94f2d")
    card.pack(fill="both", expand=True)

    ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=(25, 8))
    ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=38, weight="bold"), text_color="#FFF8E1").pack()

def create_homepage(main_area, user_id):
    for w in main_area.winfo_children():
        w.destroy()
    welcome_label = ctk.CTkLabel(main_area, text=f"Welcome back, User {user_id}!", font=ctk.CTkFont(size=28, weight="bold"))
    welcome_label.pack(pady=(30,10))
    quote_text = "“Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.”"
    quote_label = ctk.CTkLabel(main_area, text=quote_text, font=ctk.CTkFont(size=18, slant="italic"), text_color="#555", wraplength=700, justify="center")
    quote_label.pack(pady=(0,30), padx=50)
    summary_frame = ctk.CTkFrame(main_area)
    summary_frame.pack(pady=10, padx=30, fill="x")
    goals_count = len(get_goals_func(user_id))
    habits_count = 4
    pomodoro_sessions = 2

    # Create summary frame to hold cards
    summary_frame = ctk.CTkFrame(main_area, fg_color="#2d1f1f", corner_radius=25)
    summary_frame.pack(pady=30, padx=50, fill="x")

    # Example usage with your data
    create_stat_card(summary_frame, "Active Goals", goals_count)
    create_stat_card(summary_frame, "Habits Tracked", habits_count)
    create_stat_card(summary_frame, "Pomodoro Sessions", pomodoro_sessions)

    # Button frame with improved style and spacing
    btn_frame = ctk.CTkFrame(main_area, fg_color=None)
    btn_frame.pack(pady=50)

def create_nav_button(parent, text, icon, command):
    btn = ctk.CTkButton(parent, text=f"{icon}  {text}", width=200, height=65,
                        fg_color="#FF5733", hover_color="#e14e3c",
                        text_color="white", font=ctk.CTkFont(size=22, weight="bold"),
                        corner_radius=30, command=command)
    btn.pack(side="left", padx=30)
    return btn

    def logout():
        # Clear the main window to logout the user
        for widget in app.winfo_children():
            widget.destroy()

        # Show the login screen again to allow the user to switch accounts
        show_login()

    def switch_account():
        # Allow the user to switch to another account (logout and show login screen)
        logout()
    
# Function to clear placeholder text from the entry fields
def clear_placeholder(event, entry, placeholder, is_password=False):
    if entry.get() == placeholder:
        entry.delete(0, ctk.END)
        if is_password:
            entry.configure(show="*")

# Function to add placeholder text back to the entry fields
def add_placeholder(entry, placeholder, is_password=False):
    if not entry.get():
        entry.insert(0, placeholder)
        if is_password:
            entry.configure(show="")

#-----------------------------------------------------------------CODE UNTUK Goal planner----------------------------------------------------------------

def open_calendar_popup(entry):
    def set_date():
        date = cal.get_date()
        entry.delete(0, ctk.END)
        entry.insert(0, date)
        popup.destroy()

    popup = ctk.CTkToplevel()
    popup.title("Select Deadline")
    popup.geometry("300x300")
    popup.transient(entry.master)
    popup.grab_set()
    popup.focus_set()
    popup.protocol("WM_DELETE_WINDOW", popup.destroy)
    popup.resizable(False, False)

    cal = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)
    select_btn = ctk.CTkButton(popup, text="Select Date", command=set_date)
    select_btn.pack(pady=10)

def create_goal_card(parent, goal, on_edit, on_delete, on_complete):
    card = ctk.CTkFrame(parent, fg_color="#f0f0f0", corner_radius=10, border_width=1, border_color="#ccc")
    card.pack(fill="x", padx=20, pady=8)

    title_label = ctk.CTkLabel(card, text=goal["title"], font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    title_label.pack(side="top", fill="x", padx=10, pady=(10, 0))

    desc_label = ctk.CTkLabel(card, text=goal.get("description", ""), font=ctk.CTkFont(size=14), anchor="w", text_color="#555")
    desc_label.pack(side="top", fill="x", padx=10, pady=(0, 5))

    deadline_label = ctk.CTkLabel(card, text=f"Deadline: {goal.get('deadline', 'N/A')}", font=ctk.CTkFont(size=14), anchor="w", text_color="#AA0000")
    deadline_label.pack(side="top", fill="x", padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    complete_btn = ctk.CTkButton(btn_frame, text="✔ Complete", width=100, fg_color="#4CAF50", command=lambda: on_complete(goal))
    complete_btn.pack(side="left", padx=5)

    edit_btn = ctk.CTkButton(btn_frame, text="✎ Edit", width=80, fg_color="#2196F3", command=lambda: on_edit(goal))
    edit_btn.pack(side="left", padx=5)

    delete_btn = ctk.CTkButton(btn_frame, text="🗑 Delete", width=80, fg_color="#f44336", command=lambda: on_delete(goal))
    delete_btn.pack(side="right", padx=5)

    return card

def goal_planner(main_area, user_id, get_goals_func, add_goal_func, update_goal_func, delete_goal_func):
    for widget in main_area.winfo_children():
        widget.destroy()

    ctk.CTkLabel(main_area, text="Goal Planner", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=15)

    goals_container = ctk.CTkScrollableFrame(main_area, height=400)
    goals_container.pack(fill="both", expand=True, padx=20, pady=10)

    def on_edit(goal):
        popup = ctk.CTkToplevel()
        popup.title("Edit Goal")
        popup.geometry("400x350")
        popup.transient(main_area)

        scroll_frame = ctk.CTkScrollableFrame(popup)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll_frame, text="Title:").pack(pady=(20,5))
        title_entry = ctk.CTkEntry(scroll_frame)
        title_entry.insert(0, goal["title"])
        title_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(scroll_frame, text="Description:").pack(pady=(10,5))
        desc_entry = ctk.CTkEntry(scroll_frame)
        desc_entry.insert(0, goal["description"])
        desc_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(scroll_frame, text="Deadline:").pack(pady=(10,5))
        deadline_entry = ctk.CTkEntry(scroll_frame)
        deadline_entry.insert(0, goal["deadline"])
        deadline_entry.pack(pady=5, fill="x", padx=20)

        cal_btn = ctk.CTkButton(scroll_frame, text="📅 Pick Date", command=lambda: open_calendar_popup(deadline_entry))
        cal_btn.pack(pady=10)

        def save_edit():
            new_title = title_entry.get().strip()
            new_desc = desc_entry.get().strip()
            new_deadline = deadline_entry.get().strip()
            if not new_title:
                messagebox.showerror("Error", "Title cannot be empty.")
                return
            update_goal_func(goal["id"], new_title, new_desc, new_deadline)
            popup.destroy()
            refresh_goals()

        save_btn = ctk.CTkButton(scroll_frame, text="Save Changes", command=save_edit, fg_color="#4CAF50")
        save_btn.pack(pady=20)

    def on_delete(goal):
        confirm = messagebox.askyesno("Delete Goal", f"Are you sure you want to delete '{goal['title']}'?")
        if confirm:
            delete_goal_func(goal["id"])
            refresh_goals()

    def on_complete(goal):
        confirm = messagebox.askyesno("Complete Goal", f"Mark '{goal['title']}' as complete?")
        if confirm:
            delete_goal_func(goal["id"])
            refresh_goals()

    def refresh_goals():
        for child in goals_container.winfo_children():
            child.destroy()

        goals = get_goals_func(user_id)
        for g in goals:
            goal_dict = {
                "id": g[0],
                "title": g[2],
                "description": g[3],
                "deadline": g[4]
            }
            create_goal_card(goals_container, goal_dict, on_edit, on_delete, on_complete)

    create_frame = ctk.CTkFrame(main_area)
    create_frame.pack(fill="x", padx=20, pady=15)

    title_entry = ctk.CTkEntry(create_frame, placeholder_text="Goal Title")
    title_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    desc_entry = ctk.CTkEntry(create_frame, placeholder_text="Goal Description")
    desc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    deadline_entry = ctk.CTkEntry(create_frame, placeholder_text="Deadline (YYYY-MM-DD)")
    deadline_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    cal_btn = ctk.CTkButton(create_frame, text="📅", width=40, command=lambda: open_calendar_popup(deadline_entry))
    cal_btn.grid(row=0, column=3, padx=5, pady=5)

    create_frame.grid_columnconfigure(0, weight=3)
    create_frame.grid_columnconfigure(1, weight=4)
    create_frame.grid_columnconfigure(2, weight=2)

    def add_new_goal():
        title = title_entry.get().strip()
        desc = desc_entry.get().strip()
        deadline = deadline_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Goal Title cannot be empty!")
            return
        add_goal_func(user_id, title, desc, deadline)
        title_entry.delete(0, ctk.END)
        desc_entry.delete(0, ctk.END)
        deadline_entry.delete(0, ctk.END)
        refresh_goals()

    add_btn = ctk.CTkButton(create_frame, text="Add Goal", command=add_new_goal, fg_color="#4CAF50")
    add_btn.grid(row=0, column=4, padx=10, pady=5)

    refresh_goals()
#-----------------------------------------------------------------CODE UNTUK Habit builder----------------------------------------------------------------

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

def choose_color(header, sidebar, title_frame):
        # Open color picker dialog and get the selected color
        color_code = colorchooser.askcolor(title="Choose Header/Sidebar Color")[1]
        if color_code:  # If a color was selected
            # Apply the selected color to the header, sidebar, and title_frame
            header.configure(fg_color=color_code)
            sidebar.configure(fg_color=color_code)
            title_frame.configure(fg_color=color_code)
            # Also change the color of the text box
            for widget in sidebar.winfo_children():
                widget.configure(fg_color=color_code)  # Change the color of the box around the text

            # Optionally, save the color in settings or use it dynamically
            print(f"Selected color: {color_code}")
            return color_code
        return None

def settings_page(main_area, user_id, header, title, sidebar, title_frame):
        # Clear all widgets from main_area
        for widget in main_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(main_area, text="Settings", font=("Inter", 95, "bold"), text_color="black").pack(pady=40)

        # Background Color Option: Open color picker for header/sidebar
        def open_color_picker():
            color_code = choose_color(header, sidebar, title_frame)  # Pass header, sidebar, and title_frame to choose_color
            if color_code:
                # Save the selected color in the database and global variable
                save_user_settings(user_id, background_color=color_code, font_family=main_font_family[0], font_size=main_font_size[0])

        # Button to open color chooser dialog
        ctk.CTkButton(main_area, text="Choose Header/Sidebar Color", command=open_color_picker).pack(pady=20)

        # Font Family Option
        ctk.CTkLabel(main_area, text="Font Family:", font=("Inter", 40), text_color="#000000").pack(pady=10)
        font_family_selector = ctk.CTkOptionMenu(main_area, values=["Inter", "Arial", "Courier", "Times"])
        font_family_selector.pack(pady=10)

        # Font Size Option
        ctk.CTkLabel(main_area, text="Font Size:", font=("Inter", 40), text_color="#000000").pack(pady=10)
        font_size_selector = ctk.CTkOptionMenu(main_area, values=["12", "16", "32", "64", "128"])
        font_size_selector.pack(pady=10)

        # Apply Settings Button
        def apply_settings():
            new_font = font_family_selector.get()
            new_font_size = int(font_size_selector.get())

            # Apply the selected font to header, title, sidebar, etc.
            title.configure(font=ctk.CTkFont(family=new_font, size=new_font_size, weight="bold"))
            for widget in sidebar.winfo_children():
                widget.configure(font=ctk.CTkFont(family=new_font, size=new_font_size))

            for widget in main_area.winfo_children():
                widget.configure(font=ctk.CTkFont(family=new_font, size=new_font_size))

            # Save the new settings in the database
            save_user_settings(user_id, background_color=main_bg_color[0], font_family=new_font, font_size=new_font_size)

            messagebox.showinfo("Settings Applied", f"Font: {new_font} {new_font_size}")

        ctk.CTkButton(main_area, text="Apply Settings", command=apply_settings).pack(pady=30)

#------------------------------------------------------------------Daily quote ----------------------------------------------------------------


def run_app():
    global app
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("IMPROVE - MAKE LIFE BETTER")
    app.geometry("1690x900")
    app.resizable(True, True)
    show_login()
    app.mainloop()

run_app()