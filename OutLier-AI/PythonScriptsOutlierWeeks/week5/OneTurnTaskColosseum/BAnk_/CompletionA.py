import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import hashlib
import os, datetime
import re

def is_date(string):
    """Check if a string represents a date"""
    if pd.isna(string):
        return False
    
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY or M/D/YYYY
        r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD or YYYY-M-D
        r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY or M-D-YYYY
    ]
    
    string = str(string).strip()
    for pattern in date_patterns:
        if re.match(pattern, string):
            try:
                # Try to parse the date to ensure it's valid
                pd.to_datetime(string)
                return True
            except:
                continue
    return False

def extract_date_from_string(text):
    """Extract date from a string that might contain other text"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY or M/D/YYYY
        r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD or YYYY-M-D
        r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY or M-D-YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return ""

class Interface1(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.style = Style("litera")

        # Load icons
        try:
            self.icon_debit = PhotoImage(file='./lib/icon_debit.png')
            self.icon_credit = PhotoImage(file='./lib/icon_credit.png')
        except:
            self.icon_debit = None
            self.icon_credit = None

        self.tree_style = ttk.Style()
        self.tree_style.configure("Treeview.Heading", font=("Calibri", 8, "bold"))
        self.tree_style.configure("Treeview", rowheight=17)
        self.tree_style.map("Treeview", background=[("selected", "#2574D3")], foreground=[("selected", "white")])
        self.tree_style.configure("Treeview", background="#F3F3F3", fieldbackground="#F3F3F3")

        load_button = ttk.Button(self, text="Load Bank Records", bootstyle=INFO, command=self.load_records)
        load_button.pack(fill=X, padx=10, pady=10)

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, padx=10, pady=2)

        input_frame = ttk.Frame(self)
        input_frame.pack(fill=X, padx=10, pady=10)
        ttk.Label(input_frame, bootstyle="secondary", text="🔍").pack(side=LEFT, padx=5)
        ttk.Entry(input_frame).pack(side=LEFT, fill=X, expand=True, padx=5)
        ttk.Checkbutton(input_frame, text="Show Uncategorized Records Only").pack(side=LEFT, padx=5)

        # Label to display the icon
        self.icon_label = ttk.Label(input_frame)
        self.icon_label.pack(side=LEFT, padx=5)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Exclude ID, BANK, and TYPE from columns
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Record", "Date Purchased", "Date Processed", "Amount", "Explanation", "Balance", "Category", "Sub-Category", "Comments"),
            show="headings",
            bootstyle=INFO
        )

        column_widths = [5, 10, 10, 7, 70, 7, 10, 10, 10]
        for col, width in zip(self.tree["columns"], column_widths):
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))
            self.tree.column(col, width=width * 8, anchor=tk.CENTER)

        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.update_icon_state_based_on_selection)

        # Load data
        self.database_filename = "database.csv"
        self.initialize_or_load_database()

    def initialize_or_load_database(self):
        if os.path.exists(self.database_filename):
            self.database_df = pd.read_csv(self.database_filename).fillna('')
        else:
            self.database_df = pd.DataFrame(columns=[
                "Record", "Date Purchased", "Date Processed", "Amount", "Explanation", 
                "Balance", "Category", "Sub-Category", "ID", "BANK", "Type", "Comments"
            ])
            self.database_df.to_csv(self.database_filename, index=False)
            print("Database file not found. Created a new one.")

        if not self.database_df.empty and not self.database_df['ID'].is_unique:
            print("Warning: Duplicate IDs found in the DataFrame.")
        self.refresh_tree_view()

    def refresh_tree_view(self):
        """Refresh the tree view with current database data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add data to tree (excluding ID, BANK, Type columns from display)
        display_columns = ["Record", "Date Purchased", "Date Processed", "Amount", "Explanation", "Balance", "Category", "Sub-Category", "Comments"]
        for index, row in self.database_df.iterrows():
            values = [row.get(col, '') for col in display_columns]
            self.tree.insert('', 'end', values=values)

    def treeview_sort_column(self, treeview, col, reverse):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        treeview.heading(col, command=lambda: self.treeview_sort_column(treeview, col, not reverse))

    def update_icon_state_based_on_selection(self, event):
        """Update icon based on selected record type"""
        selection = self.tree.selection()
        if selection and hasattr(self, 'database_df') and not self.database_df.empty:
            item_index = self.tree.index(selection[0])
            if item_index < len(self.database_df):
                record_type = self.database_df.iloc[item_index].get('Type', '')
                if record_type == 'CreditCard' and self.icon_credit:
                    self.icon_label.config(image=self.icon_credit)
                elif record_type == 'DebitCard' and self.icon_debit:
                    self.icon_label.config(image=self.icon_debit)
                else:
                    self.icon_label.config(image='')

    def generate_md5_hash_of_row(self, row_data):
        """Generate MD5 hash of a row's data"""
        row_string = '|'.join(str(item) for item in row_data)
        return hashlib.md5(row_string.encode()).hexdigest()

    def load_records(self):
        filepath = filedialog.askopenfilename(
            title="Select a bank record file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if not filepath:
            print("No file selected.")
            return

        try:
            input_df = pd.read_csv(filepath)
            print(f"File loaded successfully with {len(input_df)} rows.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the file: {e}")
            return

        records_processed = 0
        records_skipped = 0

        for index, row in input_df.iterrows():
            row_list = row.tolist()
            print(f"Processing Row {index}: {row_list}")

            bank_pattern = self.detect_bank_pattern(row_list)
            if bank_pattern:
                result = self.process_bank_row(row_list, bank_pattern)
                if result == "processed":
                    records_processed += 1
                elif result == "skipped":
                    records_skipped += 1
            else:
                print(f"Row {index} does not match any expected pattern.")

        # Save database and refresh view
        self.database_df.to_csv(self.database_filename, index=False)
        self.refresh_tree_view()
        
        messagebox.showinfo("Processing Complete", 
                          f"Processing completed.\nRecords processed: {records_processed}\nRecords skipped (duplicates): {records_skipped}")

    def detect_bank_pattern(self, row):
        """Detect which bank pattern the row matches"""
        if len(row) < 3:
            return None

        # Pad row to ensure we have at least 4 columns
        while len(row) < 4:
            row.append(None)

        print(f"Detecting pattern for row: {row}")
        
        # BankOne Credit: Column 1 = Date, Column 2 = Amount, Column 3 = Explanation
        if (len(row) >= 3 and 
            is_date(str(row[0])) and 
            pd.api.types.is_numeric_dtype(type(row[1])) and 
            isinstance(row[2], str)):
            return "BankOne Credit"
        
        # BankOne Debit: Column 1 = Date Processed, Column 2 = Amount, Column 3 = Explanation (with date), Column 4 = Balance
        if (len(row) >= 4 and 
            is_date(str(row[0])) and 
            pd.api.types.is_numeric_dtype(type(row[1])) and 
            isinstance(row[2], str) and extract_date_from_string(row[2]) and
            pd.api.types.is_numeric_dtype(type(row[3]))):
            return "BankOne Debit"
        
        # BankTwo Credit: Column 1 = blank/null, Column 2 = Explanation, Column 3 = Amount, Column 4 = Date
        if (len(row) >= 4 and 
            (pd.isna(row[0]) or str(row[0]).strip() == '') and
            isinstance(row[1], str) and 
            pd.api.types.is_numeric_dtype(type(row[2])) and 
            is_date(str(row[3]))):
            return "BankTwo Credit"
        
        # BankTwo Debit: Column 1 = Balance, Column 2 = Explanation (with date), Column 3 = Amount, Column 4 = Date Processed
        if (len(row) >= 4 and 
            pd.api.types.is_numeric_dtype(type(row[0])) and
            isinstance(row[1], str) and extract_date_from_string(row[1]) and
            pd.api.types.is_numeric_dtype(type(row[2])) and 
            is_date(str(row[3]))):
            return "BankTwo Debit"

        return None

    def process_bank_row(self, row, pattern):
        """Process a bank row according to the detected pattern"""
        # Generate MD5 hash of the row
        row_hash = self.generate_md5_hash_of_row(row)
        
        # Check if hash already exists in database
        if row_hash in self.database_df['ID'].values:
            print(f"Record with hash {row_hash} already exists. Skipping.")
            return "skipped"
        
        # Create new record based on pattern
        new_record = {
            "Record": len(self.database_df) + 1,
            "Date Purchased": "",
            "Date Processed": "",
            "Amount": "",
            "Explanation": "",
            "Balance": "",
            "Category": "",
            "Sub-Category": "",
            "ID": row_hash,
            "BANK": "",
            "Type": "",
            "Comments": ""
        }
        
        if pattern == "BankOne Credit":
            new_record["Date Purchased"] = str(row[0])
            new_record["Amount"] = str(row[1])
            new_record["Explanation"] = str(row[2])
            new_record["Type"] = "CreditCard"
            new_record["BANK"] = "BankOne"
            
        elif pattern == "BankOne Debit":
            new_record["Date Processed"] = str(row[0])
            new_record["Amount"] = str(row[1])
            new_record["Explanation"] = str(row[2])
            new_record["Balance"] = str(row[3])
            new_record["Date Purchased"] = extract_date_from_string(row[2])
            new_record["Type"] = "DebitCard"
            new_record["BANK"] = "BankOne"
            
        elif pattern == "BankTwo Credit":
            new_record["Date Purchased"] = str(row[3])
            new_record["Amount"] = str(row[2])
            new_record["Explanation"] = str(row[1])
            new_record["Type"] = "CreditCard"
            new_record["BANK"] = "BankTwo"
            
        elif pattern == "BankTwo Debit":
            new_record["Balance"] = str(row[0])
            new_record["Explanation"] = str(row[1])
            new_record["Amount"] = str(row[2])
            new_record["Date Processed"] = str(row[3])
            new_record["Date Purchased"] = extract_date_from_string(row[1])
            new_record["Type"] = "DebitCard"
            new_record["BANK"] = "BankTwo"
        
        # Add the new record to the database
        self.database_df = pd.concat([self.database_df, pd.DataFrame([new_record])], ignore_index=True)
        print(f"Added new {pattern} record with hash {row_hash}")
        return "processed"

# Main application
if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    root.title("Bank Records Manager")
    root.geometry("1200x800")
    
    app = Interface1(root)
    root.mainloop()