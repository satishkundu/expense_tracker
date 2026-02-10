from tkinter import *
from tkinter import ttk, messagebox
import database
import charts
import export_data
from datetime import date

# Main Window
window = Tk()
window.title("Personal Expense Tracker")
window.geometry("900x600")
window.configure(bg="#f0f0f0")

# --------- Styling ---------
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("TLabel", font=("Arial", 11))
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

# --------- Functions ---------

def add_data():
    if not amount_entry.get().isdigit():
        messagebox.showerror("Error", "Amount must be number")
        return

    database.insert(
        date_entry.get(),
        category_entry.get(),
        desc_entry.get(),
        amount_entry.get(),
        type_entry.get()
    )
    view_data()
    check_budget()

def view_data():
    for row in tree.get_children():
        tree.delete(row)

    for row in database.view():
        tree.insert("", END, values=row)

def delete_data():
    try:
        selected = tree.item(tree.selection())["values"]
        database.delete(selected[0])
        view_data()
    except:
        messagebox.showerror("Error", "Select a record to delete")

def update_data():
    try:
        selected = tree.item(tree.selection())["values"]

        database.update(
            selected[0],
            date_entry.get(),
            category_entry.get(),
            desc_entry.get(),
            amount_entry.get(),
            type_entry.get()
        )
        view_data()
    except:
        messagebox.showerror("Error", "Select a record to update")

def show_chart():
    charts.show_category_chart()

def export():
    export_data.export_csv()
    messagebox.showinfo("Success", "Data Exported Successfully")

# Budget Alert
MONTHLY_BUDGET = 5000

def check_budget():
    total = database.monthly_total()
    if total > MONTHLY_BUDGET:
        messagebox.showwarning(
            "Budget Alert",
            f"Budget Exceeded!\nTotal Expense: {total}"
        )

# --------- Layout Frames ---------

title = Label(window, text="Personal Expense Tracker",
              font=("Arial", 16, "bold"), bg="#f0f0f0")
title.pack(pady=10)

input_frame = Frame(window, bg="#dfe6e9", padx=20, pady=20)
input_frame.pack(fill="x", padx=20)

table_frame = Frame(window)
table_frame.pack(pady=10)

button_frame = Frame(window, bg="#f0f0f0")
button_frame.pack(pady=10)

# --------- Input Fields ---------

Label(input_frame, text="Date").grid(row=0, column=0, padx=10, pady=5)
date_entry = ttk.Entry(input_frame)
date_entry.grid(row=0, column=1)
date_entry.insert(0, str(date.today()))

Label(input_frame, text="Category").grid(row=0, column=2, padx=10)
category_entry = ttk.Combobox(
    input_frame,
    values=["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
)
category_entry.grid(row=0, column=3)
category_entry.current(0)

Label(input_frame, text="Description").grid(row=1, column=0, padx=10)
desc_entry = ttk.Entry(input_frame)
desc_entry.grid(row=1, column=1)

Label(input_frame, text="Amount").grid(row=1, column=2, padx=10)
amount_entry = ttk.Entry(input_frame)
amount_entry.grid(row=1, column=3)

Label(input_frame, text="Type").grid(row=2, column=0, padx=10)

type_entry = ttk.Combobox(input_frame, values=["Income", "Expense"])
type_entry.grid(row=2, column=1)
type_entry.current(1)

# --------- Buttons ---------

ttk.Button(button_frame, text="Add Record", command=add_data).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Update", command=update_data).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Delete", command=delete_data).grid(row=0, column=2, padx=10)
ttk.Button(button_frame, text="Show Chart", command=show_chart).grid(row=0, column=3, padx=10)
ttk.Button(button_frame, text="Export CSV", command=export).grid(row=0, column=4, padx=10)

# --------- Table (Treeview) ---------

columns = ("ID", "Date", "Category", "Description", "Amount", "Type")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.pack()

# Load Data
view_data()

window.mainloop()
