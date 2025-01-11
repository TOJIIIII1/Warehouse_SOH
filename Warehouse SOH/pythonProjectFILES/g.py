import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Initialize the database
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY,
                    subject_code TEXT,
                    subject_name TEXT,
                    whse1_buo REAL,
                    whse1_excess REAL,
                    whse2_buo REAL,
                    whse2_excess REAL,
                    whse4_buo REAL,
                    whse4_excess REAL,
                    whse1_terumo REAL,
                    whse1_prepare REAL,
                    in_qty REAL,
                    out_qty REAL,
                    consumption REAL,
                    remarks TEXT)''')
    conn.commit()
    conn.close()


# Insert data into database
def insert_data():
    try:
        # Collect data from entry widgets
        subject_code = entry_subject_code.get()
        subject_name = entry_subject_name.get()
        whse1_buo = float(entry_whse1_buo.get())
        whse1_excess = float(entry_whse1_excess.get())
        whse2_buo = float(entry_whse2_buo.get())
        whse2_excess = float(entry_whse2_excess.get())
        whse4_buo = float(entry_whse4_buo.get())
        whse4_excess = float(entry_whse4_excess.get())
        whse1_terumo = float(entry_whse1_terumo.get())
        whse1_prepare = float(entry_whse1_prepare.get())
        in_qty = float(entry_in_qty.get())
        out_qty = float(entry_out_qty.get())
        consumption = float(entry_consumption.get())
        remarks = combobox_remarks.get()

        # Insert the data into the database
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO subjects (subject_code, subject_name, whse1_buo, whse1_excess, whse2_buo, 
                                          whse2_excess, whse4_buo, whse4_excess, whse1_terumo, whse1_prepare, 
                                          in_qty, out_qty, consumption, remarks) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (subject_code, subject_name, whse1_buo, whse1_excess, whse2_buo, whse2_excess, whse4_buo,
                   whse4_excess, whse1_terumo, whse1_prepare, in_qty, out_qty, consumption, remarks))
        conn.commit()
        conn.close()

        # Calculate sum, average, and mean
        sum_values = whse1_buo + whse1_excess + whse2_buo + whse2_excess + whse4_buo + whse4_excess + whse1_terumo + whse1_prepare + in_qty + out_qty + consumption
        avg_values = sum_values / 11  # Dividing by the number of numeric fields
        mean_values = sum_values / 11  # Same for simplicity in this case

        # Display result in labels
        label_sum.config(text=f"Sum: {sum_values}")
        label_avg.config(text=f"Average: {avg_values}")
        label_mean.config(text=f"Mean: {mean_values}")

        messagebox.showinfo("Success", "Data successfully added to the database!")

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


# Function to clear the entry fields (useful for clearing after submission)
def clear_entries():
    entry_subject_code.delete(0, tk.END)
    entry_subject_name.delete(0, tk.END)
    entry_whse1_buo.delete(0, tk.END)
    entry_whse1_excess.delete(0, tk.END)
    entry_whse2_buo.delete(0, tk.END)
    entry_whse2_excess.delete(0, tk.END)
    entry_whse4_buo.delete(0, tk.END)
    entry_whse4_excess.delete(0, tk.END)
    entry_whse1_terumo.delete(0, tk.END)
    entry_whse1_prepare.delete(0, tk.END)
    entry_in_qty.delete(0, tk.END)
    entry_out_qty.delete(0, tk.END)
    entry_consumption.delete(0, tk.END)
    combobox_remarks.set("Select")


# Function to display the Data Entry Page
def show_data_entry_page():
    frame_data_entry.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    frame_summary.grid_forget()


# Function to display the Summary Page (or another page)
def show_summary_page():
    frame_summary.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    frame_data_entry.grid_forget()


# Initialize the Tkinter window
root = tk.Tk()
root.title("Subject Data Entry")
root.geometry("1000x600")

# Create the navigation bar frame
frame_nav = tk.Frame(root, width=200, bg="#2c3e50", height=600)
frame_nav.grid(row=0, column=0, sticky="ns")

# Create buttons for navigation
btn_data_entry = tk.Button(frame_nav, text="Data Entry", command=show_data_entry_page, bg="#34495e", fg="white",
                           font=("Arial", 14), padx=20, pady=10)
btn_data_entry.grid(row=0, column=0, pady=10)

btn_summary = tk.Button(frame_nav, text="Summary", command=show_summary_page, bg="#34495e", fg="white",
                        font=("Arial", 14), padx=20, pady=10)
btn_summary.grid(row=1, column=0, pady=10)

# Create the content area
frame_data_entry = tk.Frame(root)
frame_summary = tk.Frame(root)

# Data Entry Page Components (4 Columns Layout)
label_subject_code = tk.Label(frame_data_entry, text="Subject Code")
label_subject_code.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_subject_code = tk.Entry(frame_data_entry)
entry_subject_code.grid(row=0, column=1, padx=10, pady=10)

label_subject_name = tk.Label(frame_data_entry, text="Name of Subject")
label_subject_name.grid(row=0, column=2, padx=10, pady=10, sticky="w")
entry_subject_name = tk.Entry(frame_data_entry)
entry_subject_name.grid(row=0, column=3, padx=10, pady=10)

label_whse1_buo = tk.Label(frame_data_entry, text="WHSE1 (buo)")
label_whse1_buo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_whse1_buo = tk.Entry(frame_data_entry)
entry_whse1_buo.grid(row=1, column=1, padx=10, pady=10)

label_whse1_excess = tk.Label(frame_data_entry, text="WHSE1 (excess)")
label_whse1_excess.grid(row=1, column=2, padx=10, pady=10, sticky="w")
entry_whse1_excess = tk.Entry(frame_data_entry)
entry_whse1_excess.grid(row=1, column=3, padx=10, pady=10)

label_whse2_buo = tk.Label(frame_data_entry, text="WHSE2 (buo)")
label_whse2_buo.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_whse2_buo = tk.Entry(frame_data_entry)
entry_whse2_buo.grid(row=2, column=1, padx=10, pady=10)

label_whse2_excess = tk.Label(frame_data_entry, text="WHSE2 (excess)")
label_whse2_excess.grid(row=2, column=2, padx=10, pady=10, sticky="w")
entry_whse2_excess = tk.Entry(frame_data_entry)
entry_whse2_excess.grid(row=2, column=3, padx=10, pady=10)

label_whse4_buo = tk.Label(frame_data_entry, text="WHSE4 (buo)")
label_whse4_buo.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_whse4_buo = tk.Entry(frame_data_entry)
entry_whse4_buo.grid(row=3, column=1, padx=10, pady=10)

label_whse4_excess = tk.Label(frame_data_entry, text="WHSE4 (excess)")
label_whse4_excess.grid(row=3, column=2, padx=10, pady=10, sticky="w")
entry_whse4_excess = tk.Entry(frame_data_entry)
entry_whse4_excess.grid(row=3, column=3, padx=10, pady=10)

label_whse1_terumo = tk.Label(frame_data_entry, text="WHSE1 (TERUMO)")
label_whse1_terumo.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_whse1_terumo = tk.Entry(frame_data_entry)
entry_whse1_terumo.grid(row=4, column=1, padx=10, pady=10)

label_whse1_prepare = tk.Label(frame_data_entry, text="WHSE1 (PREPARE)")
label_whse1_prepare.grid(row=4, column=2, padx=10, pady=10, sticky="w")
entry_whse1_prepare = tk.Entry(frame_data_entry)
entry_whse1_prepare.grid(row=4, column=3, padx=10, pady=10)

label_in_qty = tk.Label(frame_data_entry, text="IN")
label_in_qty.grid(row=5, column=0, padx=10, pady=10, sticky="w")
entry_in_qty = tk.Entry(frame_data_entry)
entry_in_qty.grid(row=5, column=1, padx=10, pady=10)

label_out_qty = tk.Label(frame_data_entry, text="OUT")
label_out_qty.grid(row=5, column=2, padx=10, pady=10, sticky="w")
entry_out_qty = tk.Entry(frame_data_entry)
entry_out_qty.grid(row=5, column=3, padx=10, pady=10)

label_consumption = tk.Label(frame_data_entry, text="Consumption")
label_consumption.grid(row=6, column=0, padx=10, pady=10, sticky="w")
entry_consumption = tk.Entry(frame_data_entry)
entry_consumption.grid(row=6, column=1, padx=10, pady=10)

# Remarks Dropdown
label_remarks = tk.Label(frame_data_entry, text="Remarks")
label_remarks.grid(row=6, column=2, padx=10, pady=10, sticky="w")
remarks_options = ["Select", "OK", "Not OK", "Pending"]
combobox_remarks = ttk.Combobox(frame_data_entry, values=remarks_options)
combobox_remarks.grid(row=6, column=3, padx=10, pady=10)

# Buttons for submitting data
submit_button = tk.Button(frame_data_entry, text="Submit", command=insert_data)
submit_button.grid(row=7, column=0, columnspan=4, pady=20)

# Labels to display sum, average, and mean
label_sum = tk.Label(frame_data_entry, text="Sum: ")
label_sum.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

label_avg = tk.Label(frame_data_entry, text="Average: ")
label_avg.grid(row=9, column=0, columnspan=4, padx=10, pady=10)

label_mean = tk.Label(frame_data_entry, text="Mean: ")
label_mean.grid(row=10, column=0, columnspan=4, padx=10, pady=10)

# Initialize the database
init_db()

# Start with the Data Entry Page visible
show_data_entry_page()

# Create the table (Treeview)
tree = ttk.Treeview(root, columns=("Subject Code", "Name of Subject", "WHSE1 (buo)", "WHSE1 (excess)",
                                   "WHSE2 (buo)", "WHSE2 (excess)", "WHSE4 (buo)", "WHSE4 (excess)",
                                   "WHSE1 (TERUMO)", "WHSE1 (PREPARE)", "IN", "OUT", "Consumption", "Remarks"),
                    show="headings")

# Set up column headings
for col in tree["columns"]:
    tree.heading(col, text=col)

tree.grid(row=0, column=0, padx=20, pady=20)


# Run the GUI
root.mainloop()
