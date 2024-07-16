import tkinter as tk
from tkinter import messagebox
import datetime
import tkinter.messagebox as msgbox
import csv

# Function to save data to data.csv
def save_data():
    # Get the values from the GUI fields
    type_value = type_var.get()
    date_value = date_var.get()
    category_value = category_var.get()
    description_value = description_entry.get()
    amount_value = amount_entry.get()

    # Validate the amount format
    try:
        amount = float(amount_value)
        if amount == int(amount):
            amount_value = f"{int(amount)}.00"
        else:
            amount_value = f"{amount:.2f}"
    except ValueError:
        msgbox.showwarning("Invalid Amount", "Enter a valid amount with decimals (e.g., 100.00)")
        return

    data = [type_value, date_value, category_value, description_value, amount_value]

    with open("data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if the file is empty
            writer.writerow(["Type", "Date", "Category", "Description", "Amount"])
        writer.writerow(data)

    # Show a confirmation message
    messagebox.showinfo("Success", "Data saved successfully!")
    update_records()  # Update records after saving data

# Function to clear the GUI fields
def clear_fields():
    type_var.set("Expense")
    date_var.set(datetime.date.today().strftime("%Y-%m-%d"))
    category_var.set("Fixed Expenses")
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, "0.00")

def update_categories(*args):
    selected_type = type_var.get()
    if selected_type == "Expense":
        category_dropdown['menu'].delete(0, tk.END)
        expense_categories = [
            "Fixed Expenses", "Groceries", "Health/medical", "Restaurant",
            "Transportation", "Personal", "Entertainment", "Hair",
            "Gifts", "Clothing", "Forgot to Budget", "Transfer to Savings", "Others"
        ]
        for category in expense_categories:
            category_dropdown['menu'].add_command(label=category, command=lambda cat=category: category_var.set(cat))
    elif selected_type == "Income":
        category_dropdown['menu'].delete(0, tk.END)
        income_categories = ["ICICI", "Digit", "Other"]
        for category in income_categories:
            category_dropdown['menu'].add_command(label=category, command=lambda cat=category: category_var.set(cat))

def update_records():
    records = []

    # Check if the file exists
    if not os.path.isfile("data.csv"):
        # Create the file and write the header if it doesn't exist
        with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Date", "Category", "Description", "Amount"])

    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        records = list(reader)[-10:]  # Get the last 10 records including the header

    # Clear the TextArea
    records_textarea.delete(1.0, tk.END)

    # Insert the last 10 records to the TextArea
    for record in records:
        record_text = ', '.join(record)
        records_textarea.insert(tk.END, record_text + '\n')

def create_gui():
    window = tk.Tk()
    window.title("Expense Save")
    window.geometry("800x600")

    global type_var, date_var, category_var, description_entry, amount_entry, category_dropdown, records_textarea

    type_var = tk.StringVar(window)
    type_label = tk.Label(window, text="Type:")
    type_label.grid(row=0, column=0, padx=5, pady=5)
    type_dropdown = tk.OptionMenu(window, type_var, "Expense", "Income")
    type_dropdown.grid(row=0, column=1, padx=5, pady=5)

    date_var = tk.StringVar(window)
    date_var.set(datetime.date.today().strftime("%Y-%m-%d"))
    date_label = tk.Label(window, text="Date:")
    date_label.grid(row=0, column=2, padx=5, pady=5)
    date_entry = tk.Entry(window, textvariable=date_var)
    date_entry.grid(row=0, column=3, padx=5, pady=5)

    category_var = tk.StringVar(window)
    category_label = tk.Label(window, text="Category:")
    category_label.grid(row=0, column=4, padx=5, pady=5)

    type_var.trace('w', update_categories)

    category_dropdown = tk.OptionMenu(window, category_var, "Fixed Expenses")
    category_dropdown.grid(row=0, column=5, padx=5, pady=5)

    description_label = tk.Label(window, text="Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5)
    description_entry = tk.Entry(window)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    amount_var = tk.StringVar(window)
    amount_var.set("0.00")
    amount_label = tk.Label(window, text="Amount:")
    amount_label.grid(row=1, column=2, padx=5, pady=5)
    amount_entry = tk.Entry(window, textvariable=amount_var)
    amount_entry.grid(row=1, column=3, padx=5, pady=5)

    save_button = tk.Button(window, text="Save", command=save_data)
    save_button.grid(row=2, column=4, padx=5, pady=5)

    clear_button = tk.Button(window, text="Clear", command=clear_fields)
    clear_button.grid(row=2, column=5, padx=5, pady=5)

    records_textarea = tk.Text(window, height=10, width=75)
    records_textarea.grid(row=3, column=0, columnspan=10, padx=5, pady=5)

    update_records()

    refresh_button = tk.Button(window, text="Refresh", command=update_records)
    refresh_button.grid(row=4, column=4, columnspan=2, padx=5, pady=5)

    window.mainloop()

if __name__ == '__main__':
    create_gui()
