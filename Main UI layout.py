from tkinter import Tk, Frame, Label, Button
from tkinter.ttk import Separator

# Create the main window
root = Tk()
root.title("IMPROVE - MAKE LIFE BETTER")
root.geometry("1420x1010")  # Set the window size
root.configure(bg="white")  # Set background to white

# Header
header = Frame(root, bg="white", height=80)
Label(header, text="IMPROVE - MAKE LIFE BETTER", bg="red", fg="white", font=("Arial", 20, "bold")).pack(pady=20)

# Sidebar
sidebar = Frame(root, bg="red", width=200, height=1010)  
sidebar.pack(side="left", fill="y")

# Sidebar Buttons
Button(sidebar, text="Home", bg="lightgray", fg="black", font=("Arial", 14, "bold"), borderwidth=2).pack(pady=20, fill="x")
Button(sidebar, text="Goal Planner", bg="lightgray", fg="black", font=("Arial", 14, "bold"), borderwidth=2).pack(pady=20, fill="x")
Button(sidebar, text="Habit builder", bg="lightgray", fg="black", font=("Arial", 14, "bold"), borderwidth=2).pack(pady=20, fill="x")
Button(sidebar, text="Pomodoro timer", bg="lightgray", fg="black", font=("Arial", 14, "bold"), borderwidth=2).pack(pady=20, fill="x")

# Main Content
main_content = Frame(root, bg="white" , width=215, height=311)
main_content.pack(side="right", expand=True, fill="both")

# Section 1: Planner Progression
planner_section = Frame(main_content, bg="red", highlightbackground="black", highlightthickness=2, padx=30, pady=20)
planner_section.pack(padx=20, pady=20, fill="x")
Button(planner_section, text="Your planner progression", bg="lightgray", font=("Times new roman", 18, "bold")).pack(anchor="w")

# Section 2: Weekly Habit Track
habit_section = Frame(main_content, bg="red", highlightbackground="black", highlightthickness=2, padx=30, pady=20)
habit_section.pack(padx=20, pady=20, fill="x")
Button(habit_section, text="Weekly habit track", bg="lightgray", font=("Times new roman", 18, "bold")).pack(anchor="w")

# Section 3: Pomodoro Timer
pomodoro_section = Frame(main_content, bg="red", highlightbackground="black", highlightthickness=2, padx=30, pady=20)
pomodoro_section.pack(padx=20, pady=20, fill="x")
Button(pomodoro_section, text="Pomodoro timer - Build your focus", bg="lightgray", font=("Times new roman", 18, "bold")).pack(anchor="w")

# Section 4: Diary
notes_section = Frame(main_content, bg="red", highlightbackground="black", highlightthickness=2, padx=20, pady=20)
notes_section.pack(padx=20, pady=20, fill="x")
Button(notes_section, text="Got something in mind? Write it down.", bg="lightgray", font=("Times new roman", 18, "bold")).pack(anchor="w")

root.mainloop()
