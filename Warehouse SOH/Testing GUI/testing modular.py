import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class YourClass:
    def __init__(self, root):
        self.root = root
        self.create_database()
        self.create_widgets()

    def create_widgets(self):
        """Set up the widgets for the inventory page."""
        # Create a frame for the fields
        self.fields_frame = tk.Frame(self.root)
        self.fields_frame.place(relx=0.5, rely=0.25, anchor="n", width=1200, height=300)  # Center the frame

        # Define labels for the table
        labels = [
            "ID", "Raw Code", "WHSE1 (buo)", "WHSE1 (excess)", "WHSE2 (buo)", "WHSE2 (excess)",
            "WHSE4 (buo)", "WHSE4 (excess)", "WHSE1 (TERUMO)", "WHSE1 (PREPARE)", "IN", "OUT"
        ]

        # Create a dictionary to store entry widgets
        self.create_entry = {}

        # Loop through each label to create label and entry widgets in a 4-column grid
        row = 0
        col = 0
        for index, label in enumerate(labels):
            # Create label widget
            label_widget = tk.Label(self.fields_frame, text=label, anchor='w', width=20)
            label_widget.grid(row=row, column=col, sticky='w', padx=10, pady=5)

            # Create entry widget
            entry_widget = tk.Entry(self.fields_frame, width=20)
            entry_widget.grid(row=row + 1, column=col, padx=10, pady=5)

            # Store entry widget in dictionary with label as key
            self.create_entry[label] = entry_widget

            # Update column and row to position the next entry field in 4-column grid
            col += 1
            if col == 4:  # Move to next row after every 4 columns
                col = 0
                row += 2

        # Create Add, Update, and Delete buttons to interact with the database
        add_button = tk.Button(self.root, text="Add", command=self.add_data)
        add_button.place(relx=0.25, rely=0.7, anchor="n")

        update_button = tk.Button(self.root, text="Update", command=self.update_data)
        update_button.place(relx=0.5, rely=0.7, anchor="n")

        delete_button = tk.Button(self.root, text="Delete", command=self.delete_data)
        delete_button.place(relx=0.75, rely=0.7, anchor="n")

        # Create a Treeview widget to display the data in a table format
        self.tree = ttk.Treeview(self.root, columns=("ID", "Raw Code", "WHSE1 (buo)", "WHSE1 (excess)",
                                                     "WHSE2 (buo)", "WHSE2 (excess)", "WHSE4 (buo)",
                                                     "WHSE4 (excess)", "WHSE1 (TERUMO)", "WHSE1 (PREPARE)",
                                                     "IN", "OUT"), show="headings")

        # Set column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Set column widths
        for col in self.tree["columns"]:
            self.tree.column(col, width=150)

        # Place the Treeview widget in the window, centered horizontally
        self.tree.place(relx=0.5, rely=0.8, anchor="n", width=1200, height=200)

        # Load data from the database into the table
        self.load_data()

    def create_database(self):
        """Create the SQLite database and table."""
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect('inventory_data.db')
        self.cursor = self.conn.cursor()

        # Create a table if it doesn't already exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            raw_code TEXT,
            whse1_buo TEXT,
            whse1_excess TEXT,
            whse2_buo TEXT,
            whse2_excess TEXT,
            whse4_buo TEXT,
            whse4_excess TEXT,
            whse1_terumo TEXT,
            whse1_prepare TEXT,
            in_value TEXT,
            out_value TEXT
        )
        ''')

        self.conn.commit()

    def add_data(self):
        """Add new data from entry fields to the database."""
        # Get the values from the entry fields
        raw_code = self.create_entry["Raw Code"].get().strip()

        if not raw_code:  # Check if "Raw Code" is empty
            messagebox.showerror("Input Error", "Raw Code is a required field!")
            return

        # Validate other fields to ensure they contain numeric values
        data = []
        for label in ["WHSE1 (buo)", "WHSE1 (excess)", "WHSE2 (buo)", "WHSE2 (excess)",
                      "WHSE4 (buo)", "WHSE4 (excess)", "WHSE1 (TERUMO)", "WHSE1 (PREPARE)", "IN", "OUT"]:
            value = self.create_entry[label].get().strip()
            if not value.replace(".", "", 1).isdigit():  # Check if value is numeric (allows floating point)
                messagebox.showerror("Input Error", f"{label} must be a numeric value!")
                return
            data.append(value)

        # Add Raw Code to the beginning of the data list
        data.insert(0, raw_code)

        # Insert the data into the database
        self.cursor.execute('''
        INSERT INTO inventory (
            raw_code, whse1_buo, whse1_excess, whse2_buo, whse2_excess,
            whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value, out_value
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(data))

        # Commit the changes and reset entry fields
        self.conn.commit()

        # Clear the entry fields after submission
        for entry in self.create_entry.values():
            entry.delete(0, tk.END)

        # Reload the table with the updated data
        self.load_data()

        # Notify the user that the data has been added
        messagebox.showinfo("Success", "Data added successfully!")

    def update_data(self):
        """Update data for the selected row in the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a row to update!")
            return

        # Get the values from the entry fields
        raw_code = self.create_entry["Raw Code"].get().strip()

        if not raw_code:  # Check if "Raw Code" is empty
            messagebox.showerror("Input Error", "Raw Code is a required field!")
            return

        # Validate other fields to ensure they contain numeric values
        data = []
        for label in ["WHSE1 (buo)", "WHSE1 (excess)", "WHSE2 (buo)", "WHSE2 (excess)",
                      "WHSE4 (buo)", "WHSE4 (excess)", "WHSE1 (TERUMO)", "WHSE1 (PREPARE)", "IN", "OUT"]:
            value = self.create_entry[label].get().strip()
            if not value.replace(".", "", 1).isdigit():  # Check if value is numeric (allows floating point)
                messagebox.showerror("Input Error", f"{label} must be a numeric value!")
                return
            data.append(value)

        # Add Raw Code to the beginning of the data list
        data.insert(0, raw_code)

        # Get the ID of the selected item
        item_id = self.tree.item(selected_item)["values"][0]

        # Update the data in the database
        self.cursor.execute('''
        UPDATE inventory SET 
            raw_code = ?, whse1_buo = ?, whse1_excess = ?, whse2_buo = ?, whse2_excess = ?,
            whse4_buo = ?, whse4_excess = ?, whse1_terumo = ?, whse1_prepare = ?, in_value = ?, out_value = ?
        WHERE id = ?
        ''', tuple(data) + (item_id,))

        # Commit the changes and reset entry fields
        self.conn.commit()

        # Clear the entry fields after update
        for entry in self.create_entry.values():
            entry.delete(0, tk.END)

        # Reload the table with the updated data
        self.load_data()

        # Notify the user that the data has been updated
        messagebox.showinfo("Success", "Data updated successfully!")

    def delete_data(self):
        """Delete the selected row from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a row to delete!")
            return

        # Get the ID of the selected item
        item_id = self.tree.item(selected_item)["values"][0]

        # Delete the data from the database
        self.cursor.execute('''
        DELETE FROM inventory WHERE id = ?
        ''', (item_id,))

        # Commit the changes
        self.conn.commit()

        # Reload the table with the updated data
        self.load_data()

        # Notify the user that the data has been deleted
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
    root.geometry("1500x800")  # Set the size of the window
    app = YourClass(root)
    root.mainloop()
