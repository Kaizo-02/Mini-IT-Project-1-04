import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x600")
app.title("Goal Planner")

# Sidebar
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

# Main content
content = ctk.CTkFrame(app)
content.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Title
title = ctk.CTkLabel(content, text="Welcome to Goal Planner", font=("Georgia", 24, "bold"))
title.pack(pady=10)

# Goal planner section function
def create_goal_section(master, color, placeholder):
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

# First Goal Section (Orange)
create_goal_section(content, "#FFA500", "Type your goal here")

# Second Goal Section (Green)
create_goal_section(content, "#7CFC00", "Type your next goal here")

app.mainloop()
