import tkinter as tk
from tkinter import messagebox
import self
from PIL import Image, ImageTk
import db_handler  # Import the database handler module
from Main_window import WarehouseApp  # Import the WarehouseApp class

def authenticate():
    """Handles the login button click and authenticates the user."""
    username = username_entry.get()
    password = password_entry.get()

    try:
        user = db_handler.authenticate_user(username, password)
        if user:
            root.destroy()  # Close the login window
            root2 = tk.Tk()  # Create a new Tk window for the warehouse app
            app = WarehouseApp(root2)  # Launch the WarehouseApp with the new window
            root2.mainloop()  # Run the warehouse application

        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
    except ConnectionError as ce:
        messagebox.showerror("Connection Error", ce)
    except RuntimeError as re:
        messagebox.showerror("Database Error", re)

# GUI setup
root = tk.Tk()
root.title("MASTERBATCH PHILLIPINES INC.")
root.geometry("400x500")
root.configure(bg="#FFFFFF")

# Add background image
bg_image = Image.open("red-geometric-background.jpg")  # Replace with your image file path
bg_image = bg_image.resize((400, 500))
bg_image_tk = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_image_tk)
bg_label.place(relwidth=1, relheight=1)

# Header
header = tk.Frame(root, bg="#b01e1e", height=60)
header.pack(fill=tk.X, side=tk.TOP)

header_label = tk.Label(header, text="Warehouse Inventory System", bg="#b01e1e", fg="white",
                         font=("Helvetica", 16, "bold"))
header_label.pack(side=tk.LEFT, padx=50)

# Image/logo
image = Image.open("Logo man red.png")  # Replace with your image file path
image = image.resize((140, 120))  # Resize the image to fit
image_tk = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=image_tk, bg="#FFFFFF")
image_label.pack(pady=5)

# Username label and entry
username_label = tk.Label(root, text="Username", bg="#FFFFFF", fg="black", font=("Helvetica", 12))
username_label.pack(pady=(20, 5))

username_entry = tk.Entry(root, bg="#f5f5f5", fg="black", font=("Helvetica", 12), relief="flat",
                           highlightbackground="#b01e1e", highlightthickness=2, width=20)
username_entry.pack(pady=(0, 10))

# Password label and entry
password_label = tk.Label(root, text="Password", bg="#FFFFFF", fg="black", font=("Helvetica", 12))
password_label.pack(pady=(10, 5))

password_entry = tk.Entry(root, bg="#f5f5f5", fg="black", font=("Helvetica", 12), relief="flat",
                           highlightbackground="#b01e1e", highlightthickness=2, width=20, show="*")
password_entry.pack(pady=(0, 20))

# Function to change the button color on hover
def on_enter(e):
    submit_button.config(bg="#a31a1a")  # Change background color on hover

def on_leave(e):
    submit_button.config(bg="#b01e1e")  # Reset background color when hover ends

# Submit button
submit_button = tk.Button(root, text="SUBMIT", bg="#b01e1e", fg="white", font=("Helvetica", 12, "bold"),
                           relief="flat", width=20, height=2, activebackground="#a31a1a", command=authenticate)
submit_button.pack(pady=10)

# Bind the Enter key to the authenticate function
root.bind("<Return>", lambda event: authenticate())

# Bind hover effect on the submit button
submit_button.bind("<Enter>", on_enter)
submit_button.bind("<Leave>", on_leave)

root.mainloop()
