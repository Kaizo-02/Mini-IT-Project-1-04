from importlib.resources import contents
import customtkinter as ctk
import tkinter.messagebox as messagebox

# ---Set theme---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Background color state
main_bg_color = ["grey"]



def habit_builder_page(main_content):
    habits = []

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

            def make_toggle_func(h, d):
                def toggle():
                    h["days"][d] = not h["days"][d]
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
            desc = desc_entry.get().strip()
            if title:
                habits.append({
                    "title": title,
                    "description": desc or "No description",
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


def pomodoro_timer_page(main_content):
    for widget in main_content.winfo_children():
        widget.destroy()

    timer_modes = {
        "Pomodoro": [("Work", 25 * 60), ("Break", 5 * 60)],
        "Valorant": [("Focus", 50 * 60), ("Rest", 10 * 60)],
        "Testing": [("Focus", 3), ("Rest", 3)]
    }
    current_mode = ["Pomodoro"]
    sessions = timer_modes[current_mode[0]]
    session_index = [0]
    time_left = [sessions[session_index[0]][1]]
    running = [False]
    session_counter = [0]

    def _format_time(seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def _update_session_label():
        name = sessions[session_index[0]][0]
        session_label.configure(text="Work Session" if name in ["Work", "Focus"] else "Break Time",
                                text_color="#2E86C1" if name in ["Work", "Focus"] else "#27AE60")

    def _switch_session():
        if sessions[session_index[0]][0] in ["Work", "Focus"]:
            session_counter[0] += 1
            counter_label.configure(text=f"Sessions Completed: {session_counter[0]}")
        session_index[0] = (session_index[0] + 1) % len(sessions)
        time_left[0] = sessions[session_index[0]][1]
        _update_session_label()
        timer_label.configure(text=_format_time(time_left[0]))
        status_label.configure(text=f"{sessions[session_index[0]][0]} starting...")

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

# Goal planner section function
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

def restart_login():
    global root1
    root1 = ctk.CTk()
    root1.title("IMPROVE - MAKE LIFE BETTER")
    root1.geometry("1920x1080")

    ctk.CTkLabel(root1, text="Welcome to IMPROVE", fg_color="#FF5722", text_color="white",
                 font=("Inter", 90, "bold"), height=50).pack(fill="x")

    e1 = ctk.CTkEntry(root1, width=300, font=("Inter", 20), placeholder_text="Your Username")
    e1.pack(pady=20)

    e2 = ctk.CTkEntry(root1, width=300, font=("Inter", 20), placeholder_text="Your Password", show="*")
    e2.pack(pady=20)

    ctk.CTkButton(root1, text="Login", fg_color="#FF5722", hover_color="#E64A19", text_color="white",
                  font=("Inter", 45, "bold"), command=login).pack(pady=20)

    root1.mainloop()



# Main window function
def main_window():
    global root2
    root2 = ctk.CTk()
    root2.title("IMPROVE - MAKE LIFE BETTER")
    root2.geometry("1920x1080")

    root2.grid_rowconfigure(0, weight=0, minsize=80)
    root2.grid_rowconfigure(1, weight=1)
    root2.grid_columnconfigure(0, weight=0)
    root2.grid_columnconfigure(1, weight=1)

    header = ctk.CTkFrame(master=root2, fg_color="white", height=60)
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")
    header.grid_propagate(False)
    ctk.CTkLabel(master=header, text="IMPROVE - MAKE LIFE BETTER", fg_color="red", text_color="white",
                 font=("Inter", 50, "bold")).pack(expand=True)

    sidebar = ctk.CTkFrame(master=root2, width=200, fg_color="red")
    sidebar.grid(row=1, column=0, sticky="nsew")

    main_content = ctk.CTkFrame(master=root2, fg_color=main_bg_color[0])
    main_content.grid(row=1, column=1, sticky="nsew")

    def clear_main_content():
        for widget in main_content.winfo_children():
            widget.destroy()

    def goal_planner():
        clear_main_content()
        goal_planner_page(main_content, "#FFA500", "Type your goal here")
        goal_planner_page(main_content, "#7CFC00", "Type your next goal here")

    def habit_builder():
        clear_main_content()
        habit_builder_page(main_content)

    def pomodoro_timer():
        clear_main_content()
        pomodoro_timer_page(main_content)
#--------------------------------------------------------------------------settings page-------------------------------------------------------------------------------------------
    def settings_page():
        clear_main_content()

        ctk.CTkLabel(main_content, text="Settings", font=("Inter", 95, "bold"), text_color="black").pack(pady=40)

        # Background Color Option
        ctk.CTkLabel(main_content, text="Background Color:", font=("Inter", 40,), text_color="#000000").pack(pady=10)
        color_selector = ctk.CTkOptionMenu(main_content, values=["white", "#000000", "#D3D3D3", "#5F9EA0"])
        color_selector.pack(pady=10)

        # Font Family Option
        ctk.CTkLabel(main_content, text="Font Family:", font=("Inter", 40), text_color="#000000").pack(pady=10)
        font_family_selector = ctk.CTkOptionMenu(main_content, values=["Inter", "Arial", "Courier", "Times"])
        font_family_selector.pack(pady=10)

        # Font Size Option
        ctk.CTkLabel(main_content, text="Font Size:", font=("Inter", 40), text_color="#000000").pack(pady=10)
        font_size_selector = ctk.CTkOptionMenu(main_content, values=["12", "16", "32", "64", "128"])
        font_size_selector.pack(pady=10)

        def apply_settings():
            new_bg = color_selector.get()
            new_font = font_family_selector.get()
            new_font_size = int(font_size_selector.get())

            main_bg_color[0] = new_bg
            main_content.configure(fg_color=new_bg)

            # Create new font and apply it to main content widgets
            selected_font = ctk.CTkFont(family=new_font, size=new_font_size)
            for widget in main_content.winfo_children():
                if isinstance(widget, ctk.CTkLabel) or isinstance(widget, ctk.CTkButton):
                    widget.configure(font=selected_font)

            # Confirmation
            messagebox.showinfo("Settings Applied", f"Background: {new_bg}\nFont: {new_font} {new_font_size}")

        ctk.CTkButton(main_content, text="Apply Settings", command=apply_settings).pack(pady=30)

        def exit_to_login():
            root2.destroy()     # Close the main window
            restart_login()     # Show the login window again

        ctk.CTkButton(main_content, text="Exit to Login", fg_color="#FF5722", hover_color="#E64A19",
                      text_color="white", command=exit_to_login).pack(pady=10)

    def go_to_home():
        clear_main_content()
        main_content.configure(fg_color=main_bg_color[0])
        ctk.CTkLabel(main_content, text="Home Page", font=("Inter", 95, "bold"), text_color="#000000").pack(pady=40)
        btn_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
        btn_frame.pack(pady=20)
        for btn in [
            {"text": "Track your progress", "command": goal_planner},
            {"text": "Check your habit report", "command": habit_builder},
            {"text": "Retrace your focus", "command": pomodoro_timer}
        ]:
            ctk.CTkButton(master=btn_frame, text=btn["text"], width=300, height=100, font=("Inter", 30, "bold"),
                          fg_color="#A3A1A1", hover_color="#8F8D8D", text_color="white", command=btn["command"]).pack(pady=10)

    sidebar_buttons = [
        {"text": "Home", "command": go_to_home},
        {"text": "Goal Planner", "command": goal_planner},
        {"text": "Habit Builder", "command": habit_builder},
        {"text": "Pomodoro Timer", "command": pomodoro_timer},
        {"text": "Settings", "command": settings_page}
    ]

    for btn in sidebar_buttons:
        ctk.CTkButton(master=sidebar, text=btn["text"], fg_color="lightgray", hover_color="#FF7043", text_color="black",
                      font=("Inter", 25, "bold"), border_width=2, command=btn["command"]).pack(pady=(20, 0), padx=10, fill="x")

    go_to_home()
    root2.mainloop()

# Login and startup
def login():
    root1.destroy()
    main_window()

# Login Window
root1 = ctk.CTk()
root1.title("IMPROVE - MAKE LIFE BETTER")
root1.geometry("1920x1080")

ctk.CTkLabel(root1, text="Welcome to IMPROVE", fg_color="#FF5722", text_color="white",
             font=("Inter", 90, "bold"), height=50).pack(fill="x")

e1 = ctk.CTkEntry(root1, width=300, font=("Inter", 20), placeholder_text="Your Username")
e1.pack(pady=20)

e2 = ctk.CTkEntry(root1, width=300, font=("Inter", 20), placeholder_text="Your Password", show="*")
e2.pack(pady=20)

ctk.CTkButton(root1, text="Login", fg_color="#FF5722", hover_color="#E64A19", text_color="white",
              font=("Inter", 45, "bold"), command=login).pack(pady=20)

root1.mainloop()