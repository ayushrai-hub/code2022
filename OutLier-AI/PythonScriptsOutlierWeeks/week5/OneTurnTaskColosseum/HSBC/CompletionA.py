def generate_md5_hash_of_row(self, row_list):
    """Generate MD5 hash of a row for duplicate detection"""
    row_string = ''.join(str(item) for item in row_list)
    return hashlib.md5(row_string.encode()).hexdigest()

def extract_date_from_description(self, description):
    """Extract date from description text - implement based on your specific format"""
    # This is a placeholder - you'll need to implement based on your specific date format in descriptions
    # Example: if dates are in format "DD/MM/YYYY" or "DD-MM-YYYY"
    import re
    date_pattern = r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4})\b'
    match = re.search(date_pattern, str(description))
    if match:
        return match.group(1)
    return ""

def detect_bank_pattern(self, row):
    # Ensure row has at least 4 columns
    if len(row) < 4:
        return None

    # Check for HSBC patterns (existing logic)
    if (is_date(str(row[3])) and
        pd.api.types.is_number(row[2]) and
        isinstance(row[1], str) and
        pd.isna(row[0])):
        return "HSBC Credit"
    elif (is_date(str(row[3])) and
        pd.api.types.is_number(row[2]) and
        isinstance(row[1], str) and
        pd.api.types.is_number(row[0])):
        return "HSBC Debit"
    
    # Check for MetroBank patterns
    # MetroBank Credit: Date, Amount, Description
    elif (len(row) >= 3 and
          is_date(str(row[0])) and
          pd.api.types.is_number(row[1]) and
          isinstance(row[2], str)):
        return "MetroBank Credit"
    
    # MetroBank Debit: Date, Amount, Description, Balance
    elif (len(row) >= 4 and
          is_date(str(row[0])) and
          pd.api.types.is_number(row[1]) and
          isinstance(row[2], str) and
          pd.api.types.is_number(row[3])):
        return "MetroBank Debit"

    return None

def process_metrobank_credit(self, row):
    """Process MetroBank Credit record"""
    row_hash = self.generate_md5_hash_of_row(row)
    
    # Check if record already exists
    if row_hash in self.database_df['ID'].values:
        print(f"Record already exists, skipping...")
        return
    
    # Create new record
    new_record = {
        'ID': row_hash,
        'Record': len(self.database_df) + 1,
        'Date Purchased': row[0],  # Column 1
        'Figure': row[1],          # Column 2
        'Description': row[2],     # Column 3
        'Type': 'CreditCard',
        'Date Committed': '',
        'Balance': '',
        'Category': '',
        'Sub-Category': '',
        'BANK': 'MetroBank',
        'Comments': ''
    }
    
    # Add to database
    self.database_df = pd.concat([self.database_df, pd.DataFrame([new_record])], ignore_index=True)
    print(f"Added MetroBank Credit record: {new_record['Description']}")

def process_metrobank_debit(self, row):
    """Process MetroBank Debit record"""
    row_hash = self.generate_md5_hash_of_row(row)
    
    # Check if record already exists
    if row_hash in self.database_df['ID'].values:
        print(f"Record already exists, skipping...")
        return
    
    # Extract date from description
    date_from_description = self.extract_date_from_description(row[2])
    
    # Create new record
    new_record = {
        'ID': row_hash,
        'Record': len(self.database_df) + 1,
        'Date Committed': row[0],           # Column 1
        'Figure': row[1],                   # Column 2
        'Description': row[2],              # Column 3
        'Balance': row[3],                  # Column 4
        'Date Purchased': date_from_description,  # Derived from Column 3
        'Type': 'DebitCard',
        'Category': '',
        'Sub-Category': '',
        'BANK': 'MetroBank',
        'Comments': ''
    }
    
    # Add to database
    self.database_df = pd.concat([self.database_df, pd.DataFrame([new_record])], ignore_index=True)
    print(f"Added MetroBank Debit record: {new_record['Description']}")

def process_hsbc_credit(self, row):
    """Process HSBC Credit record"""
    row_hash = self.generate_md5_hash_of_row(row)
    
    # Check if record already exists
    if row_hash in self.database_df['ID'].values:
        print(f"Record already exists, skipping...")
        return
    
    # Create new record
    new_record = {
        'ID': row_hash,
        'Record': len(self.database_df) + 1,
        'Date Purchased': row[3],  # Column 4
        'Figure': row[2],          # Column 3
        'Description': row[1],     # Column 2
        'Type': 'CreditCard',
        'Date Committed': '',
        'Balance': '',
        'Category': '',
        'Sub-Category': '',
        'BANK': 'HSBC',
        'Comments': ''
    }
    
    # Add to database
    self.database_df = pd.concat([self.database_df, pd.DataFrame([new_record])], ignore_index=True)
    print(f"Added HSBC Credit record: {new_record['Description']}")

def process_hsbc_debit(self, row):
    """Process HSBC Debit record"""
    row_hash = self.generate_md5_hash_of_row(row)
    
    # Check if record already exists
    if row_hash in self.database_df['ID'].values:
        print(f"Record already exists, skipping...")
        return
    
    # Extract date from description
    date_from_description = self.extract_date_from_description(row[1])
    
    # Create new record
    new_record = {
        'ID': row_hash,
        'Record': len(self.database_df) + 1,
        'Balance': row[0],                  # Column 1
        'Description': row[1],              # Column 2
        'Figure': row[2],                   # Column 3
        'Date Committed': row[3],           # Column 4
        'Date Purchased': date_from_description,  # Derived from Column 2
        'Type': 'DebitCard',
        'Category': '',
        'Sub-Category': '',
        'BANK': 'HSBC',
        'Comments': ''
    }
    
    # Add to database
    self.database_df = pd.concat([self.database_df, pd.DataFrame([new_record])], ignore_index=True)
    print(f"Added HSBC Debit record: {new_record['Description']}")

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

    file_hash = self.generate_md5_hash_of_file(filepath)
    print(f"MD5 hash of file: {file_hash}")

    for index, row in input_df.iterrows():
        row_list = row.tolist()
        print(f"Row {index}: {row_list}")

        bank_pattern = self.detect_bank_pattern(row_list)
        
        if bank_pattern == "MetroBank Credit":
            print("MetroBank Credit routine triggered.")
            self.process_metrobank_credit(row_list)
        elif bank_pattern == "MetroBank Debit":
            print("MetroBank Debit routine triggered.")
            self.process_metrobank_debit(row_list)
        elif bank_pattern == "HSBC Credit":
            print("HSBC Credit routine triggered.")
            self.process_hsbc_credit(row_list)
        elif bank_pattern == "HSBC Debit":
            print("HSBC Debit routine triggered.")
            self.process_hsbc_debit(row_list)
        else:
            print(f"Row {index} does not match any expected pattern.")

    # Save updated database and refresh view
    self.database_df.to_csv(self.database_filename, index=False)
    self.refresh_tree_view()
    print("File processing completed.")

def refresh_tree_view(self):
    """Refresh the tree view with current database data"""
    # Clear existing items
    for item in self.tree.get_children():
        self.tree.delete(item)
    
    # Add records to tree (exclude ID, BANK, Type columns from display)
    display_columns = ["Record", "Date Purchased", "Date Committed", "Figure", 
                      "Description", "Balance", "Category", "Sub-Category", "Comments"]
    
    for _, row in self.database_df.iterrows():
        values = [row.get(col, '') for col in display_columns]
        self.tree.insert('', 'end', values=values)
def is_date(string):
    """Check if string is a valid date"""
    try:
        pd.to_datetime(string)
        return True
    except:
        return False
