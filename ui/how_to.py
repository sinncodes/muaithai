import tkinter as tk
from PIL import Image, ImageTk
from ui.main_menu import clear_frame, show_main_menu

def show_how_to(root):
    clear_frame(root)

    tk.Label(root, text="How to Use muAIthai", font=("Arial", 16, "bold")).pack(pady=15)
    
    instructions = (
        "1. Stand in front of the camera\n"
        "2. Make sure your full body is visible\n"
        "3. Perform strikes clearly\n"
        "4. Use a well-lit room \n"
        "5. Follow the audio prompts\n"
        "6. If Southpaw, mirror this stance\n"
        "7. Make sure to stay at this angle"
    )

    tk.Label(root, text=instructions, font=("Arial", 12),
             wraplength=280, justify="left").pack(padx=20, pady=20)

    img_path = "images/howto.png"
    img = Image.open(img_path)
    img = img.resize((150, 300))
    photo = ImageTk.PhotoImage(img)

    image_label = tk.Label(root, image=photo)
    image_label.image = photo 

    image_label.pack(pady=10)

    tk.Button(root, text="⬅ Back", font=("Arial", 12),
              command=lambda: show_main_menu(root)).pack(pady=10)