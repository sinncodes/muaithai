import tkinter as tk
from globals import current_user
from auth import show_login

def clear_frame(root):
    for widget in root.winfo_children():
        widget.destroy()

def show_main_menu(root):
    from ui.custom_combos_ui import show_custom_combos
    from ui.smart_combo_ui import show_smart_combos
    from ui.options import show_options
    from ui.how_to import show_how_to
    clear_frame(root)

    #top
    tk.Button(root, text="❓ How to Use", font=("Arial", 12),
              command=lambda: show_how_to(root)).pack(pady=(10, 5), anchor="n")

    #centre
    center_frame = tk.Frame(root, bg="#f5f5f5")
    center_frame.pack(expand=True)

    def make_button(label, command):
        return tk.Button(center_frame, text=label, font=("Arial", 14),
                         width=20, height=2, bg="white", fg="black",
                         relief="raised", command=command)
    
    make_button("Custom Combos", lambda: show_custom_combos(root)).pack(pady=10)
    make_button("Smart Combos", lambda: show_smart_combos(root)).pack(pady=10)
    make_button("Options", lambda: show_options(root, lambda: clear_frame(root))).pack(pady=10)
    
    #bottom
    tk.Button(root, text="Logout", font=("Arial", 12), fg="red",
              command=lambda: show_login(root)).pack(pady=20, side="bottom")