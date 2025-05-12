import sqlite3
import customtkinter as ctk
from tkinter import Toplevel
from datetime import datetime

# Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x600")
app.title("Goal Planner")

# ====================== DATABASE ==========================
def initialize_database():
    connection = sqlite3.connect("goal_planner.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT DEFAULT 'In Progress'
        )
    """)
    connection.commit()
    connection.close()

initialize_database()

# ====================== SIDEBAR ===========================
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color="#a94442")
sidebar.pack(side="left", fill="y")

buttons = [
    ("🏠 Home", None),
    ("📍 Goal Planner", None),
    ("📅 Habit builder", None),
    ("⏱️ Pomodoro timer", None)
]

for text, command in buttons:
    btn = ctk.CTkButton(sidebar, text=text, command=command, width=180, fg_color="white", text_color="black")
    btn.pack(pady=5)

# ====================== MAIN AREA ===========================
content = ctk.CTkFrame(app)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

title = ctk.CTkLabel(content, text="Welcome to Goal Planner", font=("Georgia", 24, "bold"))
title.pack(pady=10)

# ====================== GOAL ENTRY ===========================
goal_name_entry = ctk.CTkEntry(content, placeholder_text="Enter Goal Name")
goal_name_entry.pack(pady=10)

date_label = ctk.CTkLabel(content, text="Select Due Date:")
date_label.pack()
calendar = ctk.CTkEntry(content, placeholder_text="YYYY-MM-DD")  # Using entry to simulate calendar
calendar.pack(pady=5)

def add_goal():
    goal_name = goal_name_entry.get()
    due_date = calendar.get()
    if goal_name.strip() and due_date.strip():
        conn = sqlite3.connect("goal_planner.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO goals (name, due_date) VALUES (?, ?)", (goal_name, due_date))
        conn.commit()
        conn.close()
        goal_name_entry.delete(0, ctk.END)
        calendar.delete(0, ctk.END)
        progress_tracker(goal_name)

submit_btn = ctk.CTkButton(content, text="Save Goal", command=add_goal)
submit_btn.pack(pady=10)

def progress_tracker(goal_name):
    win = Toplevel(app)
    win.title(f"Tracking: {goal_name}")
    win.geometry("400x200")

    label = ctk.CTkLabel(win, text=f"{goal_name}: 0% Complete")
    label.pack(pady=10)

    bar = ctk.CTkProgressBar(win, orientation="horizontal", mode="determinate")
    bar.pack(pady=10)
    bar.set(0)

    def update():
        val = bar.get()
        new_val = min(1.0, val + 0.1)
        bar.set(new_val)
        label.configure(text=f"{goal_name}: {int(new_val * 100)}% Complete")

    update_btn = ctk.CTkButton(win, text="Update Progress", command=update)
    update_btn.pack(pady=10)

def view_goals():
    win = Toplevel(app)
    win.title("Goal History")
    win.geometry("400x400")

    conn = sqlite3.connect("goal_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals")
    for g in cursor.fetchall():
        label = ctk.CTkLabel(win, text=f"{g[1]} - Due: {g[2]} - Status: {g[3]}")
        label.pack()
    conn.close()

history_btn = ctk.CTkButton(content, text="View Goal History", command=view_goals)
history_btn.pack(pady=10)

app.mainloop()
