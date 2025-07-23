import tkinter as tk
from logic.smart_combo_logic import generate_smart_combo
from combo_validator import validate_combo

def show_smart_combos(root):
    from ui.main_menu import show_main_menu
    combos = []

    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()

    def update_display():
        clear_frame()
        tk.Label(root, text="Smart Combo", font=("Arial", 16, "bold")).pack(pady=15)

        if combos:
            tk.Label(root, text="Combo: " + " -> ".join(combos[0]),
                     font=("Arial", 12), fg="blue").pack(pady=10)

        tk.Button(root, text="Generate New Combo", command=generate_combo).pack(pady=10)
        tk.Button(root, text="Try This Combo", command=try_combo).pack(pady=10)
        tk.Button(root, text="Back", command=lambda: show_main_menu(root)).pack(pady=20)

    def generate_combo():
        nonlocal combos
        combos = [generate_smart_combo()]
        update_display()

    def try_combo():
        if combos:
            validate_combo(combos[0])

    generate_combo()  # initial load