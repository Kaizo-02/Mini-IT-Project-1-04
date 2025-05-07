import sqlite3
import ttkbootstrap as tb
import customtkinter as CTk
from tkinter import *
from ttkbootstrap.icons import Icon
from ttkbootstrap.dialogs import Querybox
from datetime import datetime

# Initialize the database
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER,
        activity_name TEXT NOT NULL,
        progress INTEGER DEFAULT 0,
        FOREIGN KEY (goal_id) REFERENCES goals(id)
    )
    """)

    connection.commit()
    connection.close()

initialize_database()  # Call function when app starts

root = tb.Window(themename="superhero")
root.title("Goal Planner & Progress Tracker")
root.geometry('500x450')

# Goal Name Entry
goal_label = tb.Label(root, text="Enter Goal Name:")
goal_label.pack(pady=5)
goal_entry = tb.Entry(root)
goal_entry.pack(pady=5)

# Calendar Widget for Due Date
due_date_label = tb.Label(root, text="Select Due Date:")
due_date_label.pack(pady=5)
calendar = tb.DateEntry(root, bootstyle="info")
calendar.pack(pady=5)

# Function to Add Goal to DB
def add_goal():
    goal_name = goal_entry.get()
    due_date = calendar.entry.get()

    if goal_name.strip():
        connection = sqlite3.connect("goal_planner.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO goals (name, due_date) VALUES (?, ?)", (goal_name, due_date))
        connection.commit()
        connection.close()

        progress_tracker(goal_name)  # Start tracking immediately
        goal_entry.delete(0, END)

# Submit Button
submit_btn = tb.Button(root, text="Save Goal", bootstyle="success", command=add_goal)
submit_btn.pack(pady=10)

def progress_tracker(goal_name):
    tracker_window = Toplevel(root)
    tracker_window.title(f"Tracking: {goal_name}")
    tracker_window.geometry('400x300')

    # Label to Show Progress
    progress_label = tb.Label(tracker_window, text=f"{goal_name}: 0% Complete")
    progress_label.pack(pady=10)

    # Progress Bar
    progress_bar = CTk.CTkProgressBar(tracker_window, orientation="horizontal", mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar.set(0)

    # Function to Update Progress
    def update_progress():
        current_value = progress_bar.get()
        new_value = min(1.0, current_value + 0.1)  # Max at 100%
        progress_bar.set(new_value)

        percentage = int(new_value * 100)
        progress_label.config(text=f"{goal_name}: {percentage}% Complete")

    # Button to Simulate Activity Updates
    update_btn = tb.Button(tracker_window, text="Update Progress", bootstyle="primary", command=update_progress)
    update_btn.pack(pady=10)

def view_goals():
    tracker_window = Toplevel(root)
    tracker_window.title("Goal History")
    tracker_window.geometry('400x400')

    connection = sqlite3.connect("goal_planner.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM goals")
    goals = cursor.fetchall()
    connection.close()

    for goal in goals:
        tb.Label(tracker_window, text=f"{goal[1]} - Due: {goal[2]} - Status: {goal[3]}", bootstyle="secondary").pack(pady=5)

# Button to Open Goal History
history_btn = tb.Button(root, text="View Goal History", bootstyle="info", command=view_goals)
history_btn.pack(pady=10)

root.mainloop()