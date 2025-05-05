from tkinter import *
import customtkinter as ctk
from tkinter.ttk import Separator

def main_window():
    global root 
    root = Tk()
    root.title("IMPROVE - MAKE LIFE BETTER")
    root.geometry("900x600")
    root.configure(bg="#f5f5f5")

    # 📌 HEADER (Always Visible)
    header = Frame(root, bg="#f5f5f5", height=80)
    header.pack(fill="x")
    Label(header, text="IMPROVE - MAKE LIFE BETTER", fg="red", font=("Inter", 24, "bold")).pack(pady=20)

    # 📌 SIDEBAR NAVIGATION
    sidebar = Frame(root, bg="#FF5722", width=200)
    sidebar.pack(side="left", fill="y")

    Label(sidebar, text="Main Menu", bg="#FF5722", fg="black", font=("Inter", 20, "bold")).pack(pady=20)

    # 📌 MAIN CONTENT AREA
    main_content = Frame(root, bg="white")
    main_content.pack(side="right", expand=True, fill="both")

    # 📌 GOAL PLANNER FRAME (Hidden Initially)
    goal_planner_frame = Frame(main_content, bg="#FFEBEE", padx=20, pady=20)
    Label(goal_planner_frame, text="Goal Planner", font=("Arial", 18, "bold")).pack()
    goal_entry = ctk.CTkEntry(goal_planner_frame, width=300)
    goal_entry.pack()
    date_entry = ctk.CTkEntry(goal_planner_frame, width=300)
    date_entry.pack()

    Button(goal_planner_frame, text="Add Goal", command=lambda: print("Goal Added!"), bg="green").pack(pady=10)

    # 📌 PROGRESSION TRACKER & DIARY FRAME
    home_frame = Frame(main_content, bg="#FFEBEE", padx=20, pady=20)
    
    tracker_buttons = [
        "Your Planner Progression",
        "Weekly Habit Track",
        "Pomodoro Timer - Build Your Focus",
        "Got Something in Mind? Write it Down."
    ]

    for btn_text in tracker_buttons:
        Label(home_frame, text=btn_text, font=("Arial", 18, "bold")).pack(pady=10)

    # 📌 FUNCTION TO SWITCH SECTIONS WITHOUT OPENING NEW WINDOWS
    def show_goal_planner():
        for widget in main_content.winfo_children():
            widget.pack_forget()  # Hide other sections
        goal_planner_frame.pack(expand=True, fill="both")

    def show_home():
        for widget in main_content.winfo_children():
            widget.pack_forget()
        home_frame.pack(expand=True, fill="both")

    # 📌 SIDEBAR BUTTONS
    nav_buttons = [
        {"text": "Home", "command": show_home},
        {"text": "Goal Planner", "command": show_goal_planner},
        {"text": "Habit Builder", "command": lambda: print("Habit Builder")},
        {"text": "Pomodoro Timer", "command": lambda: print("Pomodoro Timer")}
    ]

    for btn in nav_buttons:
        button = Button(sidebar, text=btn["text"], bg="#A3A1A1", font=("Arial", 14), command=btn["command"])
        button.pack(pady=10, fill="x")

    # 📌 SHOW HOME PAGE ON STARTUP
    show_home()

    root.mainloop()

main_window()
