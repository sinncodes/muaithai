import tkinter as tk
from auth import show_login

root = tk.Tk()
root.title("MuAIthai")
root.geometry("400x700")

show_login(root)

root.mainloop()