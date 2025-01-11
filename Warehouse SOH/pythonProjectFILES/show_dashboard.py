import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x800")  # Set window size
        self.root.title("Inventory Management")

        # Create a left sidebar navigation frame
        self.sidebar = tk.Frame(self.root, width=200, bg="gray", height=800, relief="sunken")
        self.sidebar.pack(side="left", fill="y")

        # Buttons for navigation
        self.button2 = tk.Button(self.sidebar, text="Inventory", command=self.show_inventory)
        self.button2.pack(fill="x", padx=10, pady=10)

        self.button1 = tk.Button(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.button1.pack(fill="x", padx=10, pady=10)

        self.button3 = tk.Button(self.sidebar, text="Settings", command=self.show_settings)
        self.button3.pack(fill="x", padx=10, pady=10)

        # Create a frame to hold the content of the current page
        self.content_frame = tk.Frame(self.root, width=1300, height=800, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Create a database connection
        self.create_database()

        # Initially show the dashboard page
        self.show_dashboard()

    def create_database(self):
        """Create the SQLite database and table."""
        self.conn = sqlite3.connect('inventory_data.db')
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't already exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            raw_code TEXT,
            whse1_buo DOUBLE,
            whse1_excess DOUBLE,
            whse2_buo DOUBLE,
            whse2_excess DOUBLE,
            whse4_buo DOUBLE,
            whse4_excess DOUBLE,
            whse1_terumo DOUBLE,
            whse1_prepare DOUBLE,
            in_value DOUBLE,
            out_value DOUBLE,
            consumption DOUBLE,
            ending_balance DOUBLE
        )
        ''')
        self.conn.commit()

    def calculate_ending_balance(self, whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value):
        """Calculate the ending balance."""
        return (whse1_buo + whse1_excess + whse2_buo + whse2_excess + whse4_buo + whse4_excess + whse1_terumo + whse1_prepare + in_value - out_value)

    def show_dashboard(self):
        """Show the dashboard page."""
        # Clear the current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add widgets for Dashboard Page
        label = tk.Label(self.content_frame, text="Welcome to the Dashboard", font=("Arial", 24))
        label.pack(pady=20)

        stats_label = tk.Label(self.content_frame, text="Statistics Overview", font=("Arial", 18))
        stats_label.pack(pady=20)

        # Add more widgets for the Dashboard as needed

    def show_inventory(self):
        """Show the inventory page."""
        # Clear the current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add widgets for Inventory Page
        label = tk.Label(self.content_frame, text="Inventory Management", font=("Arial", 24))
        label.pack(pady=20)

        # Create entry fields for the inventory form in 4 columns
        fields_frame = tk.Frame(self.content_frame)
        fields_frame.pack(pady=20)

        labels = [
            "ID", "Raw Code", "WHSE1 (buo)", "WHSE1 (excess)", "WHSE2 (buo)", "WHSE2 (excess)",
            "WHSE4 (buo)", "WHSE4 (excess)", "WHSE1 (TERUMO)", "WHSE1 (PREPARE)", "IN", "OUT", "Consumption", "Ending Balance"
        ]

        # Create a dictionary to store entry widgets
        self.create_entry = {}

        # Loop through each label to create label and entry widgets in 4 columns
        for index, label in enumerate(labels):
            row = index // 4
            col = index % 4

            label_widget = tk.Label(fields_frame, text=label, anchor='w', width=20)
            label_widget.grid(row=row, column=col * 2, sticky='w', padx=10, pady=5)

            if label != "Ending Balance":  # Exclude the field for Ending Balance
                entry_widget = tk.Entry(fields_frame, width=20)
                entry_widget.grid(row=row, column=col * 2 + 1, padx=10, pady=5)
                self.create_entry[label] = entry_widget

        # Add Add, Update, Delete buttons
        button_frame = tk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        add_button = tk.Button(button_frame, text="Add", command=self.add_data)
        add_button.grid(row=0, column=0, padx=10)

        update_button = tk.Button(button_frame, text="Update", command=self.update_data)
        update_button.grid(row=0, column=1, padx=10)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_data)
        delete_button.grid(row=0, column=2, padx=10)

        # Create a treeview to display the inventory data
        self.tree = ttk.Treeview(self.content_frame, columns=labels, show="headings")
        for label in labels:
            self.tree.heading(label, text=label)
            self.tree.column(label, width=100, anchor='center')

        self.tree.pack(pady=20)

        self.load_data()

    def show_settings(self):
        """Show the settings page."""
        # Clear the current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Add widgets for Settings Page
        label = tk.Label(self.content_frame, text="Settings", font=("Arial", 24))
        label.pack(pady=20)

        # Add settings controls like checkboxes or input fields as needed
        settings_label = tk.Label(self.content_frame, text="Adjust your preferences here", font=("Arial", 18))
        settings_label.pack(pady=20)

    def add_data(self):
        """Add data from entry fields to the database."""
        raw_code = self.create_entry["Raw Code"].get()
        whse1_buo = float(self.create_entry["WHSE1 (buo)"].get() or 0)
        whse1_excess = float(self.create_entry["WHSE1 (excess)"].get() or 0)
        whse2_buo = float(self.create_entry["WHSE2 (buo)"].get() or 0)
        whse2_excess = float(self.create_entry["WHSE2 (excess)"].get() or 0)
        whse4_buo = float(self.create_entry["WHSE4 (buo)"].get() or 0)
        whse4_excess = float(self.create_entry["WHSE4 (excess)"].get() or 0)
        whse1_terumo = float(self.create_entry["WHSE1 (TERUMO)"].get() or 0)
        whse1_prepare = float(self.create_entry["WHSE1 (PREPARE)"].get() or 0)
        in_value = float(self.create_entry["IN"].get() or 0)
        out_value = float(self.create_entry["OUT"].get() or 0)
        consumption = float(self.create_entry["Consumption"].get() or 0)

        ending_balance = self.calculate_ending_balance(whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value)

        # Insert the data into the database
        self.cursor.execute('''
        INSERT INTO inventory (raw_code, whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value, consumption, ending_balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (raw_code, whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value, consumption, ending_balance))

        self.conn.commit()
        self.load_data()

        messagebox.showinfo("Success", "Data added successfully!")

    def update_data(self):
        """Update selected data in the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Row", "Please select a row to update.")
            return

        # Get the data from entry fields
        raw_code = self.create_entry["Raw Code"].get()
        whse1_buo = float(self.create_entry["WHSE1 (buo)"].get() or 0)
        whse1_excess = float(self.create_entry["WHSE1 (excess)"].get() or 0)
        whse2_buo = float(self.create_entry["WHSE2 (buo)"].get() or 0)
        whse2_excess = float(self.create_entry["WHSE2 (excess)"].get() or 0)
        whse4_buo = float(self.create_entry["WHSE4 (buo)"].get() or 0)
        whse4_excess = float(self.create_entry["WHSE4 (excess)"].get() or 0)
        whse1_terumo = float(self.create_entry["WHSE1 (TERUMO)"].get() or 0)
        whse1_prepare = float(self.create_entry["WHSE1 (PREPARE)"].get() or 0)
        in_value = float(self.create_entry["IN"].get() or 0)
        out_value = float(self.create_entry["OUT"].get() or 0)
        consumption = float(self.create_entry["Consumption"].get() or 0)

        ending_balance = self.calculate_ending_balance(whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value, consumption)

        # Get the selected row ID
        selected_row = self.tree.item(selected_item)["values"]
        row_id = selected_row[0]

        # Update data in the database
        self.cursor.execute('''
        UPDATE inventory SET raw_code=?, whse1_buo=?, whse1_excess=?, whse2_buo=?, whse2_excess=?, whse4_buo=?, whse4_excess=?, whse1_terumo=?, whse1_prepare=?, in_value=?, out_value=?, consumption=?, ending_balance=? WHERE id=?
        ''', (raw_code, whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value, consumption, ending_balance, row_id,))

        self.conn.commit()
        self.load_data()

        messagebox.showinfo("Success", "Data updated successfully!")

    def delete_data(self):
        """Delete selected data from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Row", "Please select a row to delete.")
            return

        selected_row = self.tree.item(selected_item)["values"]
        row_id = selected_row[0]

        # Delete the selected row from the database
        self.cursor.execute("DELETE FROM inventory WHERE id=?", (row_id,))
        self.conn.commit()
        self.load_data()

        messagebox.showinfo("Success", "Data deleted successfully!")

    def load_data(self):
        """Load data from the database into the Treeview table."""
        # Clear the current data in the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch the data from the database
        self.cursor.execute("SELECT * FROM inventory")
        rows = self.cursor.fetchall()

        # Insert data into the Treeview table
        for row in rows:
            self.tree.insert("", "end", values=row)

# Example to test the layout
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
