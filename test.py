import customtkinter as ctk

def toggle_menu():
    if hasattr(toggle_menu, "menu") and toggle_menu.menu.winfo_exists():
        if toggle_menu.menu.winfo_ismapped():
            toggle_menu.menu.place_forget()
        else:
            toggle_menu.menu.place(x=440, y=55)  # adjust as needed
    else:
        show_menu()

def show_menu():
    menu = ctk.CTkFrame(app, fg_color="white", width=150, height=100, corner_radius=10)
    menu.place(x=440, y=55)

    ctk.CTkButton(menu, text="Logout", command=lambda: print("Logged out"), fg_color="transparent", text_color="black").pack(pady=5)
    ctk.CTkButton(menu, text="Switch Account", command=lambda: print("Switching..."), fg_color="transparent", text_color="black").pack(pady=5)

    toggle_menu.menu = menu  # store menu so we can toggle it

app = ctk.CTk()
app.geometry("600x400")
ctk.set_appearance_mode("light")

header = ctk.CTkFrame(app, height=60, fg_color="#444")
header.pack(fill="x")

# PROFILE BUTTON
profile_btn = ctk.CTkButton(
    header, text="👤", width=40, height=40,
    fg_color="gray", text_color="white", command=toggle_menu
)
profile_btn.pack(side="right", padx=10, pady=10)

app.mainloop()
