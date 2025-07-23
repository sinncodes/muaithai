import tkinter as tk
from globals import current_user
from combo_validator import validate_combo
from logic.custom_combos_logic import STRIKES, save_user_combo

def show_custom_combos(root):
    from ui.main_menu import show_main_menu

    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()
    clear_frame()

    user_combo = current_user.get("current_combo", "")

    if user_combo:
        tk.Label(root, text="Your Saved Combo", font=("Arial", 16, "bold")).pack(pady=15)
        combo_display = user_combo.replace(",", " -> ")
        tk.Label(root, text=combo_display, font=("Arial", 14), fg="blue").pack(pady=10)

        tk.Button(root, text="Use This Combo", font=("Arial", 12),
                  command=lambda: (validate_combo(user_combo.split(",")))).pack(pady=5)

        tk.Button(root, text="Edit Combo", font=("Arial", 12),
                  command=lambda: combo_creator(root)).pack(pady=5)

        tk.Button(root, text="Back", font=("Arial", 12),
                  command=lambda: show_main_menu(root)).pack(pady=15)
    else:
        combo_creator(root)

def combo_creator(root):
    from ui.main_menu import show_main_menu

    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()
    clear_frame()

    tk.Label(root, text="Create Your Combo", font=("Arial", 16, "bold")).pack(pady=10)

    strike_vars = []

    def update_combo_preview():
        combo_preview.config(text=" - ".join([v.get() for v in strike_vars if v.get()]))

    def save_combo():
        combo = [v.get() for v in strike_vars if v.get()]
        if not save_user_combo(combo):
            feedback_label.config(text="Select at least one strike", fg="red")
        else:
            feedback_label.config(text="Combo Saved", fg="green")
    
    for i in range(5):
        var = tk.StringVar()
        strike_vars.append(var)
        tk.OptionMenu(root, var, *STRIKES, command=lambda _: update_combo_preview()).pack(pady=3)

    tk.Label(root, text="Combo Preview:", font=("Arial", 12)).pack(pady=(10, 0))
    combo_preview = tk.Label(root, text="", font=("Arial", 12), fg="blue")
    combo_preview.pack()

    feedback_label = tk.Label(root, text="", font=("Arial", 10))
    feedback_label.pack(pady=5)

    tk.Button(root, text="Save Combo", font=("Arial", 12), command=save_combo).pack(pady=5)
    tk.Button(root, text="Back", font=("Arial", 12),
              command=lambda: show_custom_combos(root)).pack(pady=10)