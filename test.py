import customtkinter as ctk

ctk.set_appearance_mode("light")

def logout():
    print("Logout clicked")
    hide_menu()

def switch_account():
    print("Switch Account clicked")
    hide_menu()

def toggle_menu():
    if menu_frame.winfo_ismapped():
        hide_menu()  # If it's visible, hide it
    else:
        place_menu()  # If it's hidden, show it

def hide_menu():
    if menu_frame.winfo_ismapped():
        print("Hiding menu")
        menu_frame.place_forget()

def place_menu():
    # Get the current window width
    window_width = app.winfo_width()

    if window_width < 900:  # If window is minimized or small, place at x=450, y=55
        print("Placing menu at x=450, y=55 for minimized window")
        x = 450
        y = 55
    else:  # If window is maximized, place at x=1390, y=55
        print("Placing menu at x=1390, y=55 for maximized window")
        x = 1390
        y = 55

    # Place the menu at the specified position
    menu_frame.place(x=x, y=y)

def on_resize(event):
    if menu_frame.winfo_ismapped():
        place_menu()  # Reposition the menu on window resize

app = ctk.CTk()
app.geometry("600x400")  # Initial window size
app.title("Profile Dropdown Example")

header = ctk.CTkFrame(app, height=60, fg_color="#333")
header.pack(fill="x")

profile_btn = ctk.CTkButton(
    header,
    text="👤",
    width=50,
    height=50,
    fg_color="gray",
    text_color="white",
    corner_radius=25,
    command=toggle_menu
)
profile_btn.pack(side="right", padx=10, pady=10)

# Create the menu frame (initially hidden)
menu_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=10)

ctk.CTkButton(menu_frame, text="Logout", command=logout, fg_color="transparent", text_color="black").pack(fill="x", pady=5, padx=10)
ctk.CTkButton(menu_frame, text="Switch Account", command=switch_account, fg_color="transparent", text_color="black").pack(fill="x", pady=5, padx=10)

# Bind window resize event to recalculate position
app.bind("<Configure>", on_resize)

app.mainloop()
