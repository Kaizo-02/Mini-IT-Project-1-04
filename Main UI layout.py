from tkinter import *
from tkinter.ttk import Separator
from pomodorocoding import PomodoroApp

def main_window():
    root2 = Tk()
    root2.title("IMPROVE - MAKE LIFE BETTER")
    root2.geometry("1420x1010")
    root2.configure(bg="#f5f5f5")

    # Header for the app
    header = Frame(root2, bg="white", height=80)
    header.pack(fill="x")
    Label(header, text="IMPROVE - MAKE LIFE BETTER", bg="#FF5722", fg="white", font=("Arial", 24, "bold")).pack(pady=20)

    # Sidebar with buttons
    sidebar = Frame(root2, bg="#FF5722", width=200)
    sidebar.pack(side="left", fill="y")

    # Sidebar Buttons 
    def on_hover(event):
        event.widget.config(bg="#E64A19")

    def on_leave(event):
        event.widget.config(bg="#FF5722")

    def go_to_home():
        print("Navigating to Home...")
    def goal_planner():
        print("Opening Goal Planner...")
    def habit_builder():
        print("Launching Habit Builder...")
    def pomodoro_timer():
        print("Starting Pomodoro Timer...")
        PomodoroApp().mainloop()
#redirection buttons
    buttons = [
        {"text": "Home", "command": go_to_home},
        {"text": "Goal Planner", "command": goal_planner},
        {"text": "Habit Builder", "command": habit_builder},
        {"text": "Pomodoro Timer", "command": pomodoro_timer}
    ]

    for btn in buttons:
        button = Button(sidebar, text=btn["text"], bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0,
                        command=btn["command"])
        button.pack(pady=10, fill="x", padx=10)
        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", on_leave)

#Area for progression features
    main_content = Frame(root2, bg="white", width=215)
    main_content.pack(side="right", expand=True, fill="both")

    sections = [
        {"title": "Your Planner Progression"},
        {"title": "Weekly Habit Track"},
        {"title": "Pomodoro Timer - Build Your Focus"},
        {"title": "Got Something in Mind? Write it Down."}
    ]

    for sec in sections:
        section_frame = Frame(main_content, bg="#FFEBEE", highlightbackground="#FFCDD2", highlightthickness=2, padx=20, pady=20)
        section_frame.pack(padx=20, pady=20, fill="x")
        Button(section_frame, text=sec["title"], bg="#FFFFFF", font=("Times New Roman", 18, "bold"), relief="flat").pack(anchor="w")

    root2.mainloop()

#login function
def login():
    username = e1.get()
    password = e2.get()
    print(f"Username: {username}, Password: {password}")
    root1.destroy()
    main_window()

# Login Window
root1 = Tk()
root1.title("IMPROVE - MAKE LIFE BETTER")
root1.geometry("700x500")
root1.configure(bg="#f5f5f5")

Label(root1, text="Welcome to IMPROVE", bg="#FF5722", fg="white", font=("Arial", 20, "bold"), height=2).pack(fill="x")

# Enter username
e1 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2)
e1.pack(pady=20)
e1.insert(0, "Your Username")

#Enter password
e2 = Entry(root1, width=30, font=("Arial", 14), borderwidth=2, show="*")
e2.pack(pady=20)
e2.insert(0, "Your Password")

# Login Button
Button(root1, text="Login", bg="#FF5722", fg="white", font=("Arial", 14, "bold"), borderwidth=0, command=login).pack(pady=20)

root1.mainloop()