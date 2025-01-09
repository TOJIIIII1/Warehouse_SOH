import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd  # Import pandas for saving to Excel

class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warehouse Inventory System")
        self.root.geometry("1400x800")

        # Database setup
        self.conn = sqlite3.connect("warehouse_inventory.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Navigation bar setup (retained across all pages)
        self.create_navigation_bar()

        # Initially show the inventory page
        self.show_inventory()

    def create_table(self):
        """Create the database table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            raw_code TEXT,
            whse1_buo REAL,
            whse1_excess REAL,
            whse2_buo REAL,
            whse2_excess REAL,
            whse4_buo REAL,
            whse4_excess REAL,
            whse1_terumo REAL,
            whse1_prepare REAL,
            in_value REAL,
            out_value REAL,
            cons REAL,
            gain REAL,
            loss REAL,
            ending_balance REAL,
            status TEXT
        )
        """)
        self.conn.commit()

    def create_navigation_bar(self):
        """Create a navigation bar that stays visible across all pages."""
        self.nav_frame = tk.Frame(self.root, bg="#b01e1e")
        self.nav_frame.place(x=0, y=200, width=200, height=800)

        tk.Button(self.nav_frame, text="Dashboard", bg="#FFFFFF", command=self.show_dashboard, width=20).pack(pady=10)
        tk.Button(self.nav_frame, text="Inventory", bg="#FFFFFF", command=self.show_inventory, width=20).pack(pady=10)
        tk.Button(self.nav_frame, text="Reports", bg="#FFFFFF", command=self.show_reports, width=20).pack(pady=10)

    def update_header(self, header_text):
        """Update the header text and center it dynamically."""
        if hasattr(self, 'header_label'):
            self.header_label.destroy()  # Destroy the old header if it exists

        self.header_label = tk.Label(self.root, text=header_text, font=("Arial", 20, "bold"))

        # Calculate the x position to center the label
        header_width = self.header_label.winfo_reqwidth()
        window_width = self.root.winfo_width()
        x_position = (window_width - header_width) // 2

        self.header_label.place(x=x_position, y=50)  # Adjust y-coordinate to position the header

    def show_inventory(self):
        """Show the inventory page."""
        self.clear_content()
        self.create_widgets()

        # Update header text for the inventory page
        self.update_header("Warehouse Inventory")

    def create_widgets(self):
        """Set up the widgets for inventory page."""
        self.fields_frame = tk.Frame(self.root)
        self.fields_frame.place(x=310, y=100, width=1180, height=300)

        labels = [
            "Raw Code", "WHSE1 (buo)", "WHSE1 (excess)", "WHSE2 (buo)", "WHSE2 (excess)",
            "WHSE4 (buo)", "WHSE4 (excess)", "WHSE1 (TERUMO)", "WHSE1 (PREPARE)", "IN",
            "OUT", "CONS", "Gain", "Loss", "Ending Balance", "Status"
        ]
        self.entries = {}

        for i, label in enumerate(labels):
            row, col = divmod(i, 4)
            tk.Label(self.fields_frame, text=label).grid(row=row, column=col * 2, padx=5, pady=5)
            entry = tk.Entry(self.fields_frame)
            entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)
            self.entries[label.lower().replace(" ", "_").replace("(", "").replace(")", "")] = entry

        # Action buttons
        self.action_frame = tk.Frame(self.root)
        self.action_frame.place(x=200, y=230, width=1180, height=50)

        tk.Button(self.action_frame, text="Delete", command=self.delete_record, bg="#dc3545", fg="white",
                  width=10).pack(side="right", padx=10)
        tk.Button(self.action_frame, text="Update", command=self.update_record, bg="#ffc107", fg="black",
                  width=10).pack(side="right", padx=10)
        tk.Button(self.action_frame, text="Add", command=self.add_record, bg="#28a745", fg="white", width=10).pack(
            side="right", padx=10)

        # Search bar for filtering inventory (Retained only on inventory page)
        self.search_label = tk.Label(self.root, text="Search:")
        self.search_label.place(x=210, y=280)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.place(x=270, y=280, width=200)
        self.search_entry.bind("<KeyRelease>", self.filter_inventory)

        # Table view with scrollbar
        self.table_frame = tk.Frame(self.root)
        self.table_frame.place(x=210, y=320, width=1180, height=400)

        self.tree = ttk.Treeview(self.table_frame, columns=labels, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        for label in labels:
            self.tree.heading(label, text=label)
            self.tree.column(label, width=100)

        self.tree.bind("<Double-1>", self.populate_fields)
        self.load_data()

        # Save and Delete buttons
        self.save_delete_frame = tk.Frame(self.root)
        self.save_delete_frame.place(x=210, y=730, width=1180, height=50)

        tk.Button(self.save_delete_frame, text="Save to Excel", command=self.save_to_excel, bg="#007bff", fg="white",
                  width=20).pack(side="right", padx=10)
        tk.Button(self.save_delete_frame, text="Delete All", command=self.delete_all_records, bg="#dc3545", fg="white",
                  width=20).pack(side="right", padx=10)

    def save_to_excel(self):
        """Save the inventory table to an Excel file."""
        try:
            query = "SELECT * FROM inventory"
            rows = self.cursor.execute(query).fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            file_name = "inventory_report.xlsx"
            df.to_excel(file_name, index=False)
            messagebox.showinfo("Success", f"Table saved successfully as {file_name}")
            self.show_reports(file_name)  # Pass the file name to the reports page
        except Exception as e:
            messagebox.showerror("Error", f"Could not save table: {e}")

    def delete_all_records(self):
        """Delete all records from the inventory table."""
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all records?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM inventory")
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Success", "All records have been deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete records: {e}")

    def filter_inventory(self, event):
        """Filter inventory based on the search query."""
        search_query = self.search_entry.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.cursor.execute("SELECT * FROM inventory"):
            if any(search_query in str(value).lower() for value in row):
                self.tree.insert("", "end", values=row)

    def load_data(self):
        """Load data from the database into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.cursor.execute("SELECT * FROM inventory"):
            self.tree.insert("", "end", values=row)

    def add_record(self):
        """Add a new record to the database."""
        raw_code = self.entries['raw_code'].get().strip()  # Get the raw code field and strip any extra spaces
        if not raw_code:  # Check if raw code is empty
            messagebox.showwarning("Missing Field", "The 'Raw Code' field is required.")
            return
        try:
            values = [self.entries[field].get() for field in self.entries]
            self.cursor.execute("""
            INSERT INTO inventory (
                raw_code, whse1_buo, whse1_excess, whse2_buo, whse2_excess,
                whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, in_value,
                out_value, cons, gain, loss, ending_balance, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, values)
            self.conn.commit()
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Record added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add record: {e}")

    def update_record(self):
        """Update an existing record in the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Record", "Please select a record to update.")
            return

        try:
            record_id = self.tree.item(selected_item, "values")[0]
            values = [self.entries[field].get() for field in self.entries] + [record_id]
            self.cursor.execute("""
            UPDATE inventory SET
                raw_code=?, whse1_buo=?, whse1_excess=?, whse2_buo=?, whse2_excess=?,
                whse4_buo=?, whse4_excess=?, whse1_terumo=?, whse1_prepare=?, in_value=?,
                out_value=?, cons=?, gain=?, loss=?, ending_balance=?, status=? 
            WHERE id=?
            """, values)
            self.conn.commit()
            self.load_data()
            self.clear_fields()
            messagebox.showinfo("Success", "Record updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update record: {e}")

    def delete_record(self):
        """Delete a selected record from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Select Record", "Please select a record to delete.")
            return

        try:
            record_id = self.tree.item(selected_item, "values")[0]
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
            if confirm:
                self.cursor.execute("DELETE FROM inventory WHERE id=?", (record_id,))
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Success", "Record deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete record: {e}")

    def populate_fields(self, event):
        """Populate entry fields with selected table row data."""
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, "values")[1:]
        for i, field in enumerate(self.entries):
            self.entries[field].delete(0, tk.END)
            self.entries[field].insert(0, values[i])

    def clear_fields(self):
        """Clear all entry fields."""
        for field in self.entries:
            self.entries[field].delete(0, tk.END)

    def show_dashboard(self):
        """Show the dashboard with some statistics."""
        self.clear_content()

        # Create some dummy statistics for the dashboard
        total_items = len(self.cursor.execute("SELECT * FROM inventory").fetchall())
        total_value = sum(row[10] + row[11] for row in self.cursor.execute("SELECT * FROM inventory"))

        # Dashboard header
        self.update_header("Warehouse Dashboard")

        # Statistics display
        stats_frame = tk.Frame(self.root)
        stats_frame.place(x=210, y=100, width=1180, height=100)

        tk.Label(stats_frame, text=f"Total Items: {total_items}", font=("Arial", 16)).pack(pady=10)
        tk.Label(stats_frame, text=f"Total Value: {total_value:.2f}", font=("Arial", 16)).pack(pady=10)

    def show_reports(self):
        """Show the reports page and display exported Excel files in a table format with real-time search."""
        self.clear_content()
        self.update_header("Reports")

        # Frame for the search bar
        tk.Label(self.root, text="Search:", font=("Arial", 12)).place(x=210, y=155)
        self.search_entry = tk.Entry(self.root, font=("Arial", 12))
        self.search_entry.place(x=270, y=155, width=200)
        self.search_entry.bind("<KeyRelease>", self.filter_reports)

        # Frame for the table
        reports_frame = tk.Frame(self.root)
        reports_frame.place(x=210, y=200, width=1180, height=400)

        # Table to display the list of exported files
        columns = ("File Name", "Path", "Date Created", "Time Created")
        self.reports_tree = ttk.Treeview(reports_frame, columns=columns, show="headings")
        self.reports_tree.pack(side="left", fill="both", expand=True)

        # Define column headings
        self.reports_tree.heading("File Name", text="File Name")
        self.reports_tree.heading("Path", text="Path")
        self.reports_tree.heading("Date Created", text="Date Created")
        self.reports_tree.heading("Time Created", text="Time Created")

        # Set column widths
        self.reports_tree.column("File Name", width=300)
        self.reports_tree.column("Path", width=600)
        self.reports_tree.column("Date Created", width=150)
        self.reports_tree.column("Time Created", width=150)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(reports_frame, orient="vertical", command=self.reports_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.reports_tree.configure(yscrollcommand=scrollbar.set)

        # Load the exported files into the table
        self.report_files = self.get_exported_files()
        self.populate_reports_table(self.report_files)

        # Add action buttons below the table
        button_frame = tk.Frame(self.root)
        button_frame.place(x=210, y=520, width=1180, height=50)

        tk.Button(button_frame, text="Open Selected", command=self.open_selected_file,
                  bg="#007bff", fg="white", width=20).pack(side="left", padx=10)
        tk.Button(button_frame, text="Save Selected As", command=self.save_selected_file,
                  bg="#28a745", fg="white", width=20).pack(side="left", padx=10)

    def populate_reports_table(self, files):
        """Populate the reports table with a given list of files."""
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)  # Clear existing table content

        for file_path in files:
            file_name = os.path.basename(file_path)
            creation_time = os.path.getctime(file_path)
            date_created = datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d")
            time_created = datetime.fromtimestamp(creation_time).strftime("%H:%M:%S")
            self.reports_tree.insert("", "end", values=(file_name, file_path, date_created, time_created))

    def filter_reports(self, event=None):
        """Filter the reports table dynamically as the user types in the search box."""
        query = self.search_entry.get().strip().lower()
        filtered_files = [file for file in self.report_files if query in os.path.basename(file).lower()]
        self.populate_reports_table(filtered_files)

    def get_exported_files(self):
        """Retrieve a list of exported Excel files in the current directory."""
        try:
            current_dir = os.getcwd()
            return [os.path.join(current_dir, f) for f in os.listdir(current_dir) if f.endswith(".xlsx")]
        except Exception as e:
            messagebox.showerror("Error", f"Could not retrieve files: {e}")
            return []

    def open_selected_file(self):
        """Open the selected file from the reports table."""
        selected_item = self.reports_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a file to open.")
            return

        file_path = self.reports_tree.item(selected_item, "values")[1]
        try:
            os.startfile(file_path)  # Open the file using the default application
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def save_selected_file(self):
        """Save the selected file to a user-chosen location."""
        selected_item = self.reports_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a file to save.")
            return

        file_path = self.reports_tree.item(selected_item, "values")[1]
        try:
            save_path = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                     title="Save As",
                                                     defaultextension=".xlsx",
                                                     filetypes=[("Excel files", "*.xlsx")])
            if save_path:
                with open(file_path, "rb") as src_file:
                    with open(save_path, "wb") as dest_file:
                        dest_file.write(src_file.read())
                messagebox.showinfo("Success", f"File successfully saved as: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")
    def clear_content(self):
        """Clear the content of the current page."""
        for widget in self.root.winfo_children():
            if widget != self.nav_frame:
                widget.destroy()


# Main code to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
