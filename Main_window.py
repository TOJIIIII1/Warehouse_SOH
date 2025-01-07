import tkinter as tk

def launch_main(self):
    """Opens a new independent window and centers it on the screen."""
    # Create an independent main window
    new_window = tk.Tk()
    new_window.title("Dashboard")

    # Desired dimensions for the new window
    width = 1000
    height = 500

    # Get the screen width and height
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry with the calculated position and dimensions
    new_window.geometry(f"{width}x{height}+{x}+{y}")

    # Add a label in the new window
    label = tk.Label(new_window, text="Welcome to the Dashboard!", font=("Helvetica", 16))
    label.pack(pady=20)

    # Add a button to close the new window
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack(pady=10)

    new_window.mainloop()  # Start the event loop for the new window
