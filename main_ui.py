import customtkinter as ctk

# ---Set theme--
ctk.set_default_color_theme("blue")


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

    import tkinter.messagebox as messagebox

    # ------------------------------------------------------------------------------------- Timer Config ------------------------------------------------------#easy to spot #trust
    timer_modes = {
        "Pomodoro": [("Work", 25 * 60), ("Break", 5 * 60)],
        "Valorant": [("Focus", 50 * 60), ("Rest", 10 * 60)],
        "Testing": [("Focus", 1 * 3), ("Rest", 1 * 3)]
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

    #starts UI layout 
    # frame to switch buttons and modes and add timer custom 
    top_frame = ctk.CTkFrame(main_content, fg_color="transparent")
    top_frame.pack(anchor="nw", padx=20, pady=10)

    ctk.CTkLabel(top_frame, text="Mode:", font=("Inter", 18, "bold")).pack(side="left", padx=(0,5))

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

    main_content = ctk.CTkFrame(master=root2, fg_color="white")
    main_content.grid(row=1, column=1, sticky="nsew")

    def clear_main_content():
        for widget in main_content.winfo_children():
            widget.destroy()

    def goal_planner():
        clear_main_content()
        ctk.CTkLabel(main_content, text="Goal Planner Page", font=("Inter", 24, "bold")).pack(pady=20)

    def habit_builder():
        clear_main_content()
        habit_builder_page(main_content)

    def pomodoro_timer():
        clear_main_content()
        pomodoro_timer_page(main_content)

    def go_to_home():
        clear_main_content()
        ctk.CTkLabel(main_content, text="Home Page", font=("Inter", 95, "bold"), text_color="#2E86C1").pack(pady=40)
        btn_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
        btn_frame.pack(pady=20)
        for btn in [
            {"text": "Goal Planner", "command": goal_planner},
            {"text": "Habit Builder", "command": habit_builder},
            {"text": "Pomodoro Timer", "command": pomodoro_timer}
        ]:
            ctk.CTkButton(master=btn_frame, text=btn["text"], width=300, height=100, font=("Inter", 30, "bold"),
                          fg_color="#A3A1A1", hover_color="#8F8D8D", text_color="white", command=btn["command"]).pack(pady=10)

    for btn in [
        {"text": "Home", "command": go_to_home},
        {"text": "Goal Planner", "command": goal_planner},
        {"text": "Habit Builder", "command": habit_builder},
        {"text": "Pomodoro Timer", "command": pomodoro_timer}
    ]:
        ctk.CTkButton(master=sidebar, text=btn["text"], fg_color="lightgray", hover_color="#FF7043", text_color="black",
                      font=("Inter", 25, "bold"), border_width=2, command=btn["command"]).pack(pady=(20, 0), padx=10, fill="x")

    go_to_home()
    root2.mainloop()


def login():
    root1.destroy()
    main_window()


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
