import tkinter as tk
import sqlite3
from globals import current_user

def show_login(root):
    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()

    clear_frame()
    tk.Label(root, text="Login", font=("Arial", 18)).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    error_label = tk.Label(root, text="", fg="red", font=("Arial", 10))
    error_label.pack(pady=5)

    def handle_login():
        from ui.main_menu import show_main_menu
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            current_user.update({
    "username": result[0],
    "password": result[1],
    "stance": result[2],
})
            show_main_menu(root)
        else:
            error_label.config(text="Incorrect username or password.")

    tk.Button(root, text="Login", command=handle_login).pack(pady=5)
    tk.Button(root, text="Register", command=lambda: show_register(root)).pack(pady=5)

def show_register(root):
    def clear_frame():
        for widget in root.winfo_children():
            widget.destroy()

    clear_frame()
    tk.Label(root, text="Register", font=("Arial", 18)).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    message_label = tk.Label(root, text="", font=("Arial", 10))
    message_label.pack(pady=5)

    def handle_register():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            message_label.config(text="Both fields are required.", fg="red")
            return

        try:
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            message_label.config(text="Account created! You can now log in.", fg="green")
        except sqlite3.IntegrityError:
            message_label.config(text="Username already exists.", fg="red")

    tk.Button(root, text="Register", command=handle_register).pack(pady=5)
    tk.Button(root, text="Back to Login", command=lambda: show_login(root)).pack()