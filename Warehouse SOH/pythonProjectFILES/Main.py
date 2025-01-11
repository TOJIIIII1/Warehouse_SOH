# ui.py

import tkinter as tk
from show_dashboard import show_dashboard
from show_data import show_data
from show_reports import show_reports

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Inventory System")
        self.root.geometry("1400x800")

        # Navigation bar setup (retained across all pages)
        self.create_navigation_bar()

    def create_navigation_bar(self):
        """Create a navigation bar that stays visible across all pages."""
        self.nav_frame = tk.Frame(self.root, bg="#b01e1e")
        self.nav_frame.place(x=0, y=200, width=200, height=800)

        tk.Button(self.nav_frame, text="Dashboard", bg="#FFFFFF", command=self.show_dashboard, width=20).pack(pady=10)
        tk.Button(self.nav_frame, text="Processed Data", bg="#FFFFFF", command=self.show_data, width=20).pack(pady=10)
        tk.Button(self.nav_frame, text="Reports", bg="#FFFFFF", command=self.show_reports, width=20).pack(pady=10)

    def update_header(self, header_text):
        """Update the header text and center it dynamically."""
        if hasattr(self, 'header_label'):
            self.header_label.destroy()  # Destroy the old header if it exists

        self.header_label = tk.Label(self.root, text=header_text, font=("Arial", 20, "bold"))
        self.header_label.place(relx=0.5, rely=0.1, anchor="center")  # Center the label in the window

    def center_header(self, event):
        """Reposition header dynamically when the window is resized."""
        if hasattr(self, 'header_label'):
            header_width = self.header_label.winfo_reqwidth()
            window_width = self.root.winfo_width()

            # Recalculate the x position to center the header
            x_position = (window_width - header_width) // 2
            self.header_label.place(x=x_position, rely=0.1, anchor="center")

    # Now bind the methods properly to the class using self
    def show_dashboard(self):
        show_dashboard(self)

    def show_data(self):
        show_data(self)

    def show_reports(self):
        show_reports(self)


# Main code to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
