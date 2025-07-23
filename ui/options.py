import tkinter as tk
from globals import current_user

def show_options(content_frame, clear_content):
    from ui.main_menu import show_main_menu

    clear_content()
    tk.Label(content_frame, text="Options", font=("Arial", 18)).pack(pady=10)

    #current stance (default to "orthodox")
    stance_var = tk.StringVar(value=current_user.get("stance", "orthodox"))

    tk.Label(content_frame, text="Select Stance:").pack(pady=5)
    tk.Radiobutton(content_frame, text="Orthodox", variable=stance_var, value="orthodox").pack()
    tk.Radiobutton(content_frame, text="Southpaw", variable=stance_var, value="southpaw").pack()

    def save_options():
        current_user["stance"] = stance_var.get()
        show_main_menu(content_frame)

    tk.Button(content_frame, text="Save", command=save_options).pack(pady=10)