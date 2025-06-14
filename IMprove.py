import customtkinter as ctk
from tkinter import messagebox, colorchooser
import database as db
from tkcalendar import Calendar
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
import random

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
    users = db.get_users()

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
        db.add_user(username, email, hashed_password)
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

#----------------------------------------------------------------CODE UNTUK Quotes----------------------------------------------------------------
QUOTES = [
    "“Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.”",
    "“The only way to do great work is to love what you do.” – Steve Jobs",
    "“Strive not to be a success, but rather to be of value.” – Albert Einstein",
    "“The mind is everything. What you think you become.” – Buddha",
    "“The best way to predict the future is to create it.” – Peter Drucker",
    "“Success is not final, failure is not fatal: it is the courage to continue that counts.” – Winston S. Churchill",
    "“It always seems impossible until it’s done.” – Nelson Mandela",
    "“What you get by achieving your goals is not as important as what you become by achieving your goals.” – Zig Ziglar",
    "“The future belongs to those who believe in the beauty of their dreams.” – Eleanor Roosevelt",
    "“The greatest glory in living lies not in never falling, but in rising every time we fall.” – Nelson Mandela",
    "“The way to get started is to quit talking and begin doing.” – Walt Disney",
    "“If you look at what you have in life, you'll always have more. If you look at what you don't have in life, you'll never have enough.” – Oprah Winfrey",
    "“If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.” – James Cameron",
    "“You may be disappointed if you fail, but you are doomed if you don't try.” – Beverly Sills",
    "“Life is what happens when you’re busy making other plans.” – John Lennon"
]

QUOTE_DATA_FILE = "daily_quote_data.json" # File to store the last shown quote info

def get_daily_quote():
    """
    Retrieves a motivational quote that refreshes daily.
    It saves the last displayed quote's index and date to a JSON file.
    """
    today = datetime.now().date()
    data = {"last_date": None, "quote_index": -1} # Default values

    # Try to load existing data from file
    try:
        with open(QUOTE_DATA_FILE, 'r') as f:
            loaded_data = json.load(f)
            # Convert string date back to date object for comparison
            data["last_date"] = datetime.strptime(loaded_data["last_date"], "%Y-%m-%d").date()
            data["quote_index"] = loaded_data["quote_index"]
    except (FileNotFoundError, json.JSONDecodeError):
        # File not found or corrupted, proceed with default values (which will trigger a new quote)
        pass 
    
    selected_quote_index = data["quote_index"]

    # Check if it's a new day or if no quote has been selected yet
    if data["last_date"] is None or data["last_date"] < today:
        # It's a new day or first run, pick a new random quote
        # Ensure the new quote is different from the previous one if possible and there are multiple quotes
        if len(QUOTES) > 1 and selected_quote_index != -1:
            new_index = selected_quote_index
            while new_index == selected_quote_index:
                new_index = random.randrange(len(QUOTES))
            selected_quote_index = new_index
        else:
            selected_quote_index = random.randrange(len(QUOTES)) # Fallback for first run or single quote

        # Save the new data to the file
        try:
            with open(QUOTE_DATA_FILE, 'w') as f:
                json.dump({
                    "last_date": today.strftime("%Y-%m-%d"), # Store date as string
                    "quote_index": selected_quote_index
                }, f)
        except IOError as e:
            print(f"Error saving quote data to file: {e}")
            # If saving fails, still return the newly chosen random quote for this session
            return QUOTES[selected_quote_index]
    
    # Ensure the retrieved index is valid (in case of manual file corruption)
    if not (0 <= selected_quote_index < len(QUOTES)):
        selected_quote_index = random.randrange(len(QUOTES))
        # Attempt to re-save the corrected index
        try:
            with open(QUOTE_DATA_FILE, 'w') as f:
                json.dump({
                    "last_date": today.strftime("%Y-%m-%d"),
                    "quote_index": selected_quote_index
                }, f)
        except IOError as e:
            print(f"Error re-saving corrected quote data: {e}")


    return QUOTES[selected_quote_index]

# ----------------------------------------------------------------CODE UNTUK MAIN PAGE----------------------------------------------------------------

def get_greeting(username): 
    """Personal Greeting Based on Time of Day and Username"""
    current_hour = datetime.now().hour
    if current_hour < 12:
        return f"Good Morning, {username}"
    elif 12 <= current_hour < 18:
        return f"Good Afternoon, {username}"
    else:
        return f"Good Evening, {username}"


def show_main(user_id):
    global app
    for widget in app.winfo_children():
        widget.destroy()

    # Add a motivational quote section
    quote_frame = ctk.CTkFrame(app)
    quote_frame.pack(fill="x", pady=10)  # Add some padding
    
    daily_quote_text = get_daily_quote() # Get the quote that refreshes daily

    motivational_quote = ctk.CTkLabel(quote_frame,
                                      text=daily_quote_text, # Use the daily quote text here
                                      font=(font_family, 14, "italic"), text_color="black")
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

    # Function to clear main area when switching pages
    def clear_main_area():
        for widget in main_area.winfo_children():
            widget.destroy()
            
    create_homepage(main_area, user_id)  # Show the homepage by default

    # Function to show the home page
def create_homepage(main_area, user_id):
    """ Create a simple dashboard on the homepage with key stats and navigation buttons. """
    
    # Clear all widgets from the main area
    for widget in main_area.winfo_children():
        widget.destroy()

    # Add a greeting message
    username = db.get_username(user_id)
    greeting_label = ctk.CTkLabel(main_area, text=get_greeting(username), font=ctk.CTkFont(size=28, weight="bold"))
    greeting_label.pack(pady=(30, 10))
    
    # Add a subtitle
    ctk.CTkLabel(main_area, text="Welcome to your personalized dashboard!", font=ctk.CTkFont(size=18)).pack(pady=(0, 20))

    # Create the dashboard frame
    dashboard_frame = ctk.CTkFrame(main_area, fg_color="white", corner_radius=15)
    dashboard_frame.pack(pady=20, padx=50, fill="x", expand=True)
    dashboard_labels = {} 

    active_goals_count = db.get_active_goals_count(user_id)
    habits_tracked_count = db.get_habits_tracked_count(user_id)
    pomodoro_sessions_count = db.get_pomodoro_sessions_count(user_id)
    total_time_tracked_seconds = db.get_total_time_tracked(user_id)
    total_time_tracked_formatted = db.format_seconds_to_hms(total_time_tracked_seconds)

    # Add the statistics
    create_stat_card(dashboard_frame, "Active Goals", active_goals_count)
    create_stat_card(dashboard_frame, "Habits Tracked", habits_tracked_count)
    create_stat_card(dashboard_frame, "Pomodoro Sessions completed", pomodoro_sessions_count)
    create_stat_card(dashboard_frame, "Total Time Tracked", total_time_tracked_formatted)
    
    def update_total_time_display():
        total_seconds = db.get_total_time_tracked(user_id)
        # Ensure db.format_seconds_to_hms exists or define it here
        formatted_time = db.format_seconds_to_hms(total_seconds) 
        
        # Access the label using the stored reference and update its text
        if 'total_time_label' in dashboard_labels:
            dashboard_labels['total_time_label'].configure(text=formatted_time)

    def reset_total_time():
        if messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset your total tracked time? This action cannot be undone.", parent=main_area):
            success = db.delete_timers_by_user(user_id) # Call new DB function
            if success:
                messagebox.showinfo("Reset Successful", "Your total tracked time has been reset to 0.", parent=main_area)
                update_total_time_display() # Update the UI immediately
            else:
                messagebox.showerror("Reset Failed", "Could not reset total tracked time. Please try again.", parent=main_area)

    reset_button = ctk.CTkButton(main_area, text="Reset Total Time",
                                  command=reset_total_time,
                                  fg_color="#11DE3A",  # Red color for reset
                                  hover_color="#C0392B",
                                  text_color="white")
    reset_button.pack(pady=10)

    def update_total_time_display():
        total_seconds = db.get_total_time_tracked(user_id)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

    update_total_time_display()

    
def create_stat_card(parent, title, value):
    """ Create a stat card for the dashboard showing key statistics. """
    
    # Create a card frame
    card = ctk.CTkFrame(parent, fg_color="#FF5733", border_width=2, border_color="#d94f2d", corner_radius=10)
    card.pack(fill="both", expand=True, padx=10, pady=5)

    # Create stat card content
    ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=25)
    ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=38, weight="bold"), text_color="#FFF8E1").pack()

    # Add hover effect on the card
    card.bind("<Enter>", lambda e, btn=card: card.configure(fg_color="#FF6F60"))
    card.bind("<Leave>", lambda e, btn=card: card.configure(fg_color="#FF5733"))

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

def create_stat_card(parent, title, value):
    """ Create Stat Cards for the Homepage with Hover Effect """
    card = ctk.CTkFrame(parent, fg_color="#FF5733", border_width=2, border_color="#d94f2d", corner_radius=10)
    card.pack(fill="both", expand=True, padx=10, pady=5)

    # Add hover effect to the card
    card.bind("<Enter>", lambda e, btn=card: card.configure(fg_color="#FF6F60"))
    card.bind("<Leave>", lambda e, btn=card: card.configure(fg_color="#FF5733"))

    ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color="white").pack(pady=25)
    ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=38, weight="bold"), text_color="#FFF8E1").pack()

#-----------------------------------------------------------------CODE UNTUK Goal planner----------------------------------------------------------------

def get_goals_func(user_id: int) -> List[Dict]:
    return db.get_goals(user_id)

def add_goal_func(user_id: int, goal_text: str, description: Optional[str], due_date_str: str) -> Optional[int]:
    return db.add_goal(user_id, goal_text, description, due_date_str)

def update_goal_func(goal_id: int, user_id: int, goal_text: str, description: Optional[str], due_date_str: str) -> bool:
    return db.update_goal(goal_id, user_id, goal_text, description, due_date_str)

def delete_goal_func(goal_id: int) -> bool:
    return db.delete_goal_from_db(goal_id)

def complete_goal_func(goal_id: int) -> bool:
    return db.complete_goal(goal_id)

def open_calendar_popup(entry: ctk.CTkEntry):
    def set_date():
        selected_date = cal.get_date()
        entry.delete(0, ctk.END)
        entry.insert(0, selected_date)
        popup.destroy()

    popup = ctk.CTkToplevel()
    popup.title("Select Due Date")
    popup.geometry("300x300")
    popup.transient(entry.master)
    popup.grab_set()
    popup.focus_set()
    popup.protocol("WM_DELETE_WINDOW", popup.destroy)
    popup.resizable(False, False)

    try:
        initial_date = datetime.strptime(entry.get(), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        initial_date = datetime.now().date()

    cal = Calendar(popup, selectmode='day', date_pattern='yyyy-mm-dd',
                   year=initial_date.year, month=initial_date.month, day=initial_date.day)
    cal.pack(pady=20)
    select_btn = ctk.CTkButton(popup, text="Select Date", command=set_date)
    select_btn.pack(pady=10)

def create_goal_card(parent: ctk.CTkFrame, goal_data: Dict, on_edit: Callable, on_delete: Callable, on_complete: Callable):
    card = ctk.CTkFrame(parent, fg_color="#f0f0f0", corner_radius=10, border_width=1, border_color="#ccc")
    card.pack(fill="x", padx=10, pady=5)

    title_label = ctk.CTkLabel(card, text=goal_data["goal"], font=ctk.CTkFont(size=18, weight="bold"), anchor="w")
    title_label.pack(side="top", fill="x", padx=10, pady=(10, 0))

    description_text = goal_data.get("description")
    if description_text:
        desc_label = ctk.CTkLabel(card, text=description_text, font=ctk.CTkFont(size=14), anchor="w", text_color="#555")
        desc_label.pack(side="top", fill="x", padx=10, pady=(0, 5))

    status = goal_data.get('status', 'due')
    due_date_text = goal_data.get('due_date', 'N/A')

    date_info_text = f"Due: {due_date_text}"
    status_color = "#4CAF50"
    if status == "overdue":
        status_color = "#D32F2F"
    elif status == "due":
        status_color = "#FF9800"

    deadline_label = ctk.CTkLabel(card, text=f"{date_info_text} ({status.capitalize()})",
                                  font=ctk.CTkFont(size=14, weight="bold" if status != "complete" else "normal"),
                                  anchor="w", text_color=status_color)
    deadline_label.pack(side="top", fill="x", padx=10, pady=(0, 10))

    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    complete_btn = ctk.CTkButton(btn_frame, text="✔ Complete", width=100, fg_color="#4CAF50",
                                 command=lambda: on_complete(goal_data["goal_id"]))
    if status == "complete":
        complete_btn.configure(state="disabled", text="Completed")
    complete_btn.pack(side="left", padx=5)

    edit_btn = ctk.CTkButton(btn_frame, text="✎ Edit", width=80, fg_color="#2196F3",
                             command=lambda: on_edit(goal_data))
    edit_btn.pack(side="left", padx=5)

    delete_btn = ctk.CTkButton(btn_frame, text="🗑 Delete", width=80, fg_color="#f44336",
                               command=lambda: on_delete(goal_data["goal_id"]))
    delete_btn.pack(side="right", padx=5)

    return card

def goal_planner(main_area, user_id, get_goals_func, add_goal_func, update_goal_func, delete_goal_func):
    for widget in main_area.winfo_children():
        widget.destroy()

    ctk.CTkLabel(main_area, text="🎯 Goal Planner", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=15)

    goals_container = ctk.CTkScrollableFrame(main_area, height=400, fg_color="transparent")
    goals_container.pack(fill="both", expand=True, padx=20, pady=10)

    def on_edit_goal_ui(goal_data: Dict):
        popup = ctk.CTkToplevel()
        popup.title("Edit Goal")
        popup.geometry("400x380")
        popup.transient(main_area)
        popup.grab_set()
        popup.focus_set()
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)

        scroll_frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(scroll_frame, text="Goal Title:").pack(pady=(20,5))
        title_entry = ctk.CTkEntry(scroll_frame)
        title_entry.insert(0, goal_data["goal"])
        title_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(scroll_frame, text="Description:").pack(pady=(10,5))
        desc_entry = ctk.CTkEntry(scroll_frame)
        desc_entry.insert(0, goal_data.get("description", ""))
        desc_entry.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(scroll_frame, text="Due Date (YYYY-MM-DD):").pack(pady=(10,5))
        due_date_entry = ctk.CTkEntry(scroll_frame)
        due_date_entry.insert(0, goal_data["due_date"])
        due_date_entry.pack(pady=5, fill="x", padx=20)

        cal_btn = ctk.CTkButton(scroll_frame, text="📅 Pick Date", command=lambda: open_calendar_popup(due_date_entry))
        cal_btn.pack(pady=10)

        def save_edit():
            new_title = title_entry.get().strip()
            new_desc = desc_entry.get().strip()
            new_due_date = due_date_entry.get().strip()

            if not new_title:
                messagebox.showerror("Validation Error", "Goal title cannot be empty.")
                return
            if not new_due_date:
                messagebox.showerror("Validation Error", "Due date cannot be empty.")
                return
            try:
                datetime.strptime(new_due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid due date format. Please use 'YYYY-MM-DD'.")
                return

            if update_goal_func(goal_data["goal_id"], user_id, new_title, new_desc, new_due_date):
                messagebox.showinfo("Success", "Goal updated successfully!")
                popup.destroy()
                refresh_goals_display()
            else:
                messagebox.showerror("Database Error", "Failed to update goal.")

        save_btn = ctk.CTkButton(scroll_frame, text="Save Changes", command=save_edit, fg_color="#4CAF50")
        save_btn.pack(pady=20)

    def on_delete_goal_ui(goal_id: int):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this goal?")
        if confirm:
            delete_goal_func(goal_id)
            messagebox.showinfo("Success", "Goal deleted successfully!")
            refresh_goals_display()

    def on_complete_goal_ui(goal_id: int):
        confirm = messagebox.askyesno("Confirm Completion", "Mark this goal as complete?")
        if confirm:
            if complete_goal_func(goal_id):
                messagebox.showinfo("Success", "Goal marked as complete!")
                refresh_goals_display()
            else:
                messagebox.showerror("Database Error", "Failed to complete goal.")

    def refresh_goals_display():
        for child in goals_container.winfo_children():
            child.destroy()

        goals = get_goals_func(user_id)

        if not goals:
            ctk.CTkLabel(goals_container, text="No goals added yet. Start planning!", text_color="#777",
                         font=ctk.CTkFont(size=16)).pack(pady=50)
            return

        for goal_data in goals:
            create_goal_card(goals_container, goal_data, on_edit_goal_ui, on_delete_goal_ui, on_complete_goal_ui)

    create_frame = ctk.CTkFrame(main_area)
    create_frame.pack(fill="x", padx=20, pady=15)

    title_entry = ctk.CTkEntry(create_frame, placeholder_text="Goal Title")
    title_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    desc_entry = ctk.CTkEntry(create_frame, placeholder_text="Goal Description (Optional)")
    desc_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    due_date_entry = ctk.CTkEntry(create_frame, placeholder_text="Due Date (YYYY-MM-DD)")
    due_date_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

    cal_btn = ctk.CTkButton(create_frame, text="📅", width=40, command=lambda: open_calendar_popup(due_date_entry))
    cal_btn.grid(row=0, column=3, padx=5, pady=5)

    create_frame.grid_columnconfigure(0, weight=3)
    create_frame.grid_columnconfigure(1, weight=4)
    create_frame.grid_columnconfigure(2, weight=2)
    create_frame.grid_columnconfigure(3, weight=0)
    create_frame.grid_columnconfigure(4, weight=1)

    def add_new_goal():
        title = title_entry.get().strip()
        desc = desc_entry.get().strip()
        due_date = due_date_entry.get().strip()

        if not title:
            messagebox.showerror("Validation Error", "Goal Title cannot be empty!")
            return
        if not due_date:
            messagebox.showerror("Validation Error", "Due Date cannot be empty!")
            return
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid due date format. Please use 'YYYY-MM-DD'.")
            return

        add_goal_func(user_id, title, desc, due_date)
        messagebox.showinfo("Success", f"Goal '{title}' added successfully!")
        title_entry.delete(0, ctk.END)
        desc_entry.delete(0, ctk.END)
        due_date_entry.delete(0, ctk.END)
        refresh_btn = ctk.CTkButton(create_frame, text="🔄 Refresh Goals", command=refresh_goals_display, fg_color="#2196F3"
                                )
        refresh_goals_display()

    


    add_btn = ctk.CTkButton(create_frame, text="➕ Add Goal", command=add_new_goal, fg_color="#4CAF50")
    add_btn.grid(row=0, column=4, padx=10, pady=5)
    refresh_goals_display()
#-----------------------------------------------------------------CODE UNTUK Habit builder----------------------------------------------------------------

def habit_builder_page(main_content, user_id):
    for widget in main_content.winfo_children():
        widget.destroy()

    raw_habits = db.get_habits(user_id)
    all_completions = db.get_habit_completions(user_id)
    completion_map = {}
    for habit_id, comp_date_str in all_completions:
        if habit_id not in completion_map:
            completion_map[habit_id] = set()
        completion_map[habit_id].add(comp_date_str)


    habits_data_model = []
    for habit_row in raw_habits:
        habit_id = habit_row[0]
        description = habit_row[1]
        habit_name = habit_row[2]

        days_status = {}
        for i in range(7):
            date_obj = datetime.now().date() - timedelta(days=6 - i)
            date_str = date_obj.strftime('%Y-%m-%d')
            days_status[date_str] = date_str in completion_map.get(habit_id, set())

        habits_data_model.append({
            "id": habit_id,
            "title": habit_name,
            "description": description,
            "days_completion": days_status
        })

    def draw_habits():
        for widget in habit_list_frame.winfo_children():
            widget.destroy()

        if not habits_data_model:
            ctk.CTkLabel(habit_list_frame, text="No habits added yet. Click 'Create new habit +' to start!",
                         font=ctk.CTkFont(size=20), text_color="#555555").pack(pady=50)
            return

        for habit in habits_data_model:
            habit_card = ctk.CTkFrame(habit_list_frame, fg_color="#d9d9d9", corner_radius=10)
            habit_card.pack(anchor="nw", padx=20, pady=10, fill="x")

            habit_title = ctk.CTkLabel(habit_card, text=habit["title"], font=ctk.CTkFont(size=45), text_color="black")
            habit_title.pack(anchor="nw", padx=10, pady=(10, 0))

            habit_subtext = ctk.CTkLabel(habit_card, text=habit["description"], font=ctk.CTkFont(size=30), text_color="black")
            habit_subtext.pack(anchor="nw", padx=10, pady=(0, 10))

            days_header_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
            days_header_frame.pack(anchor="nw", padx=10, pady=(0,0))
            for i in range(7):
                date_obj = datetime.now().date() - timedelta(days=6 - i)
                day_name = date_obj.strftime('%a')
                ctk.CTkLabel(days_header_frame, text=day_name, text_color="black", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)

            circle_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
            circle_frame.pack(anchor="nw", padx=10, pady=(0, 10))

            def make_toggle_func(habit_id_val, date_str_val):
                def toggle():
                    if db.mark_habit_complete(habit_id_val, user_id, date_str_val):
                        messagebox.showinfo("Habit", f"Habit marked complete for {date_str_val}!", parent=main_content)
                    else:
                        if messagebox.askyesno("Habit", f"Habit already complete for {date_str_val}. Unmark?", parent=main_content):
                            db.unmark_habit_complete(habit_id_val, user_id, date_str_val)
                            messagebox.showinfo("Habit", f"Habit unmarked for {date_str_val}.", parent=main_content)
                        else:
                            return

                    update_habits_data_model()
                    draw_habits()
                return toggle

            for date_str, is_complete in habit["days_completion"].items():
                color = "#28A745" if is_complete else "#d1b5b5"
                if date_str == datetime.now().date().strftime('%Y-%m-%d'):
                    ctk.CTkButton(circle_frame, text="", width=30, height=30, corner_radius=15, fg_color=color,
                                  hover_color="#1E7E34" if not is_complete else "#7d6b6b",
                                  command=make_toggle_func(habit["id"], date_str)).pack(side="left", padx=10)
                else:
                    # For previous days, show as disabled buttons (no toggle)
                    ctk.CTkButton(circle_frame, text="", width=30, height=30, corner_radius=15, fg_color=color,
                                  state="disabled").pack(side="left", padx=10)



            action_frame = ctk.CTkFrame(habit_card, fg_color="#d9d9d9")
            action_frame.pack(anchor="ne", padx=10, pady=(0, 10), fill="x")

            def delete_habit_command(habit_id_to_delete, habit_title_to_delete):
                if messagebox.askyesno("Delete Habit", f"Are you sure you want to delete '{habit_title_to_delete}'? This cannot be undone.", parent=main_content):
                    if db.delete_habit(habit_id_to_delete, user_id):
                        messagebox.showinfo("Habit Deleted", f"'{habit_title_to_delete}' has been deleted.", parent=main_content)
                        update_habits_data_model()
                        draw_habits()
                    else:
                        messagebox.showerror("Error", f"Failed to delete '{habit_title_to_delete}'.", parent=main_content)

            ctk.CTkButton(action_frame, text="Delete Habit", fg_color="#E74C3C", hover_color="#C0392B",
                          command=lambda h_id=habit["id"], h_title=habit["title"]: delete_habit_command(h_id, h_title)).pack(side="right", padx=10)


    def update_habits_data_model():
        """Refreshes the habits_data_model from the database."""
        nonlocal habits_data_model

        raw_habits = db.get_habits(user_id)
        all_completions = db.get_habit_completions(user_id)
        completion_map = {}
        for habit_id, comp_date_str in all_completions:
            if habit_id not in completion_map:
                completion_map[habit_id] = set()
            completion_map[habit_id].add(comp_date_str)

        new_habits_data_model = []
        for habit_row in raw_habits:
            habit_id = habit_row[0]
            description = habit_row[1]
            habit_name = habit_row[2]

            days_status = {}
            for i in range(7):
                date_obj = datetime.now().date() - timedelta(days=6 - i)
                date_str = date_obj.strftime('%Y-%m-%d')
                days_status[date_str] = date_str in completion_map.get(habit_id, set())
            new_habits_data_model.append({
                "id": habit_id,
                "title": habit_name,
                "description": description,
                "days_completion": days_status
            })
        habits_data_model[:] = new_habits_data_model


    def open_add_habit_popup():
        popup = ctk.CTkToplevel(main_content)
        popup.title("Add New Habit")
        popup.geometry("400x250")
        popup.attributes('-topmost', True)
        popup.grab_set()

        ctk.CTkLabel(popup, text="Habit Title:", font=ctk.CTkFont(size=16)).pack(pady=(10,0))
        title_entry = ctk.CTkEntry(popup, placeholder_text="e.g., Enter your habit title here")
        title_entry.pack(pady=(0,10), padx=20, fill="x")

        ctk.CTkLabel(popup, text="Description (Optional):", font=ctk.CTkFont(size=16)).pack(pady=(10,0))
        desc_entry = ctk.CTkEntry(popup, placeholder_text="e.g., Enter a brief description of your habit")
        desc_entry.pack(pady=(0,20), padx=20, fill="x")

        def save_habit():
            title = title_entry.get().strip()
            desc = desc_entry.get().strip()
            if not title:
                messagebox.showerror("Input Error", "Habit title cannot be empty.", parent=popup)
                return

            new_habit_id = db.add_habit(desc, title, user_id)
            if new_habit_id:
                messagebox.showinfo("Success", f"Habit '{title}' added successfully!", parent=popup)
                update_habits_data_model()
                draw_habits()
                popup.destroy()


        ctk.CTkButton(popup, text="Add Habit", command=save_habit,
                      fg_color="#28A745", hover_color="#218838", text_color="white").pack(pady=10)
        popup.transient(main_content.winfo_toplevel())
        popup.wait_window(popup)


    title_label = ctk.CTkLabel(main_content, text="Habit Builder", font=ctk.CTkFont(size=95, weight="bold"), text_color="black")
    title_label.pack(anchor="nw", padx=20, pady=(20, 10))

    create_btn = ctk.CTkButton(main_content, text="Create new habit +", fg_color="#A3A1A1", text_color="black",
                                 hover_color="#8F8D8D", command=open_add_habit_popup)
    create_btn.pack(anchor="nw", padx=20, pady=(0, 20))

    habit_list_frame = ctk.CTkScrollableFrame(main_content, fg_color="transparent")
    habit_list_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

    update_habits_data_model()
    draw_habits()

#-----------------------------------------------------------------CODE UNTUK Pomodoro timer----------------------------------------------------------------

def pomodoro_timer_page(main_content, user_id):
        for widget in main_content.winfo_children():
            widget.destroy()

        # Load saved modes from DB and merge with defaults
        saved_modes = db.load_timer_modes(user_id)
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
            h, m = divmod(m, 60)
            return f"{h:02d}:{m:02d}:{s:02d}"

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
                    db.add_timers(task, start_time_val, end_time, duration, completed, user_id)
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
            popup.geometry("400x400") # Increased height for more fields
            popup.attributes('-topmost', True)
            popup.grab_set()

            ctk.CTkLabel(popup, text="New Mode Name:").pack(pady=(10,0))
            name_entry = ctk.CTkEntry(popup, placeholder_text="e.g., Deep Work, Short Break")
            name_entry.pack(pady=(0,10))

            # Focus duration inputs
            ctk.CTkLabel(popup, text="Focus/Work Duration (HH:MM:SS):").pack(pady=(10,0))
            focus_frame = ctk.CTkFrame(popup, fg_color="transparent")
            focus_frame.pack()
            focus_h_entry = ctk.CTkEntry(focus_frame, width=60, placeholder_text="HH")
            focus_h_entry.pack(side="left", padx=2)
            ctk.CTkLabel(focus_frame, text=":").pack(side="left")
            focus_m_entry = ctk.CTkEntry(focus_frame, width=60, placeholder_text="MM")
            focus_m_entry.pack(side="left", padx=2)
            ctk.CTkLabel(focus_frame, text=":").pack(side="left")
            focus_s_entry = ctk.CTkEntry(focus_frame, width=60, placeholder_text="SS")
            focus_s_entry.pack(side="left", padx=2)

            # Rest duration inputs
            ctk.CTkLabel(popup, text="Rest/Break Duration (HH:MM:SS):").pack(pady=(10,0))
            rest_frame = ctk.CTkFrame(popup, fg_color="transparent")
            rest_frame.pack()
            rest_h_entry = ctk.CTkEntry(rest_frame, width=60, placeholder_text="HH")
            rest_h_entry.pack(side="left", padx=2)
            ctk.CTkLabel(rest_frame, text=":").pack(side="left")
            rest_m_entry = ctk.CTkEntry(rest_frame, width=60, placeholder_text="MM")
            rest_m_entry.pack(side="left", padx=2)
            ctk.CTkLabel(rest_frame, text=":").pack(side="left")
            rest_s_entry = ctk.CTkEntry(rest_frame, width=60, placeholder_text="SS")
            rest_s_entry.pack(side="left", padx=2)
            
            def parse_time_input(h_entry, m_entry, s_entry):
                try:
                    h = int(h_entry.get().strip() or 0)
                    m = int(m_entry.get().strip() or 0)
                    s = int(s_entry.get().strip() or 0)
                    if not (0 <= m < 60 and 0 <= s < 60 and h >= 0):
                        raise ValueError("Minutes and seconds must be between 0-59. Hours must be non-negative.")
                    return h * 3600 + m * 60 + s
                except ValueError as e:
                    messagebox.showerror("Input Error", f"Invalid time format: {e}", parent=popup)
                    return None
            
            def save_custom():
                try:
                    name = name_entry.get().strip()
                    focus_h = int(focus_h_entry.get().strip() or "0")
                    focus_m = int(focus_m_entry.get().strip() or "0")
                    focus_s = int(focus_s_entry.get().strip() or "0")
                    rest_h = int(rest_h_entry.get().strip() or "0")
                    rest_m = int(rest_m_entry.get().strip() or "0")
                    rest_s = int(rest_s_entry.get().strip() or "0")
                    focus_total = focus_h * 3600 + focus_m * 60 + focus_s
                    rest_total = rest_h * 3600 + rest_m * 60 + rest_s
                    if name and focus_total > 0 and rest_total > 0:
                        # Save to DB
                        db.save_timer_mode(name, focus_total, rest_total, user_id)
                        # Update in-memory dict & UI
                        timer_modes[name] = [("Focus", focus_total), ("Rest", rest_total)]
                        mode_options.append(name)
                        mode_menu.configure(values=mode_options)
                        popup.destroy()
                    else:
                        messagebox.showerror("Error", "Please enter valid values!")
                except ValueError:
                    messagebox.showerror("Error", "Hours, minutes, and seconds must be integers!")

            ctk.CTkButton(popup, text="Save Timer", command=save_custom).pack(pady=20)

        def delete_selected_mode():
            selected_mode = mode_menu.get()
            default_modes = ["Pomodoro"] # Adjust this list if you have more default modes
            if selected_mode in default_modes:
                messagebox.showinfo("Cannot Delete", "Default timer modes cannot be deleted.", parent=main_content)
                return

            if selected_mode not in timer_modes:
                messagebox.showerror("Error", f"Mode '{selected_mode}' not found.", parent=main_content)
                return

            response = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete the '{selected_mode}' timer mode?\nThis action cannot be undone.",
                parent=main_content
            )
            if response:
                try:
                    db.delete_timer_mode(selected_mode, user_id)
                    del timer_modes[selected_mode]

                    mode_options = list(timer_modes.keys())
                    mode_menu.configure(values=mode_options)

                    if current_mode[0] == selected_mode:
                        if "Pomodoro" in timer_modes:
                            mode_menu.set("Pomodoro")
                            switch_mode("Pomodoro")
                        elif mode_options:
                            mode_menu.set(mode_options[0])
                            switch_mode(mode_options[0])
                        else:
                            messagebox.showinfo("No Modes Left", "All custom timer modes have been deleted. Reverting to default Pomodoro.", parent=main_content)
                            timer_modes["Pomodoro"] = [("Work", 25 * 60), ("Break", 5 * 60)]
                            mode_options = list(timer_modes.keys())
                            mode_menu.configure(values=mode_options)
                            mode_menu.set("Pomodoro")
                            switch_mode("Pomodoro")

                    messagebox.showinfo("Deleted", f"Timer mode '{selected_mode}' has been deleted.", parent=main_content)

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete timer mode: {e}", parent=main_content)


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
        
        ctk.CTkButton(top_frame, text="🗑️ Delete Selected Mode", command=delete_selected_mode,
                    fg_color="#E74C3C", hover_color="#C0392B", text_color="white").pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="Reset", width=300, height=100, font=("Inter", 30, "bold"), fg_color="#A3A1A1",
                    hover_color="#8F8D8D", text_color="white", command=reset_timer).pack(side="left", padx=20)

        status_label = ctk.CTkLabel(timer_frame, text="Ready", font=("Inter", 20), text_color="#888888")
        status_label.pack(pady=10)

        _update_session_label()


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

#------------------------------------------------------------------Run app ----------------------------------------------------------------
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