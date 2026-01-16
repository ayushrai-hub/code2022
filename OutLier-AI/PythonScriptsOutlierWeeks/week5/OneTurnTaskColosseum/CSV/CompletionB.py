import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom

def load_csv(csv_file):
    """Load CSV with semicolon delimiter and return data"""
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        # Use semicolon as delimiter
        reader = csv.DictReader(csvfile, delimiter=';')
        data = list(reader)
        # Print available columns for debugging
        if data:
            print("Available columns:", list(data[0].keys()))
        return data

def create_base_xml():
    """Create a base XML structure"""
    root = ET.Element("Document")
    # Add any namespace or attributes your XML needs
    return root

def add_transaction_to_xml(root, row):
    """Add a single transaction to the XML"""
    try:
        # Create a new CdtTrfTxInf element for each row
        cdt_trf_tx_inf = ET.SubElement(root, 'CdtTrfTxInf')
        
        # Add <PmtId><EndToEndId> with debtor number
        pmt_id = ET.SubElement(cdt_trf_tx_inf, 'PmtId')
        end_to_end_id = ET.SubElement(pmt_id, 'EndToEndId')
        
        # Try different possible column names for debtor number
        debtor_number = None
        for key in row.keys():
            if 'debtor' in key.lower() and 'number' in key.lower():
                debtor_number = row[key]
                break
        
        if debtor_number is None:
            # Fallback - show available keys
            raise KeyError(f"Could not find debtor number column. Available columns: {list(row.keys())}")
        
        end_to_end_id.text = "XYZ " + str(debtor_number)
        
        # Add <Amt><InstdAmt> with Total Price
        amt = ET.SubElement(cdt_trf_tx_inf, 'Amt')
        instd_amt = ET.SubElement(amt, 'InstdAmt', Ccy="EUR")
        
        # Try different possible column names for total price
        total_price = None
        for key in row.keys():
            if 'total' in key.lower() and 'price' in key.lower():
                total_price = row[key]
                break
            elif 'price' in key.lower():
                total_price = row[key]
                break
            elif 'amount' in key.lower():
                total_price = row[key]
                break
        
        if total_price is None:
            raise KeyError(f"Could not find total price column. Available columns: {list(row.keys())}")
        
        # Remove currency symbols and clean the price
        clean_price = str(total_price).replace('$', '').replace('€', '').replace(',', '.').strip()
        instd_amt.text = clean_price
        
        # Add <Cdtr><Nm> with account owner
        cdtr = ET.SubElement(cdt_trf_tx_inf, 'Cdtr')
        nm = ET.SubElement(cdtr, 'Nm')
        
        # Try different possible column names for account owner
        account_owner = None
        for key in row.keys():
            if 'account' in key.lower() and 'owner' in key.lower():
                account_owner = row[key]
                break
            elif 'owner' in key.lower():
                account_owner = row[key]
                break
            elif 'name' in key.lower():
                account_owner = row[key]
                break
        
        if account_owner is None:
            raise KeyError(f"Could not find account owner column. Available columns: {list(row.keys())}")
        
        nm.text = str(account_owner)
        
        # Add <CdtrAcct><Id> with IBAN
        cdtr_acct = ET.SubElement(cdt_trf_tx_inf, 'CdtrAcct')
        id_elem = ET.SubElement(cdtr_acct, 'Id')
        
        # Try different possible column names for IBAN
        iban = None
        for key in row.keys():
            if 'iban' in key.lower():
                iban = row[key]
                break
            elif 'account' in key.lower() and 'number' in key.lower():
                iban = row[key]
                break
        
        if iban is None:
            raise KeyError(f"Could not find IBAN column. Available columns: {list(row.keys())}")
        
        id_elem.text = str(iban)
        
        # Add <RmtInf><Ustrd> with Invoice Id
        rmt_inf = ET.SubElement(cdt_trf_tx_inf, 'RmtInf')
        ustrd = ET.SubElement(rmt_inf, 'Ustrd')
        
        # Try different possible column names for Invoice ID
        invoice_id = None
        for key in row.keys():
            if 'invoice' in key.lower() and 'id' in key.lower():
                invoice_id = row[key]
                break
            elif 'invoice' in key.lower():
                invoice_id = row[key]
                break
            elif 'id' in key.lower():
                invoice_id = row[key]
                break
        
        if invoice_id is None:
            raise KeyError(f"Could not find Invoice ID column. Available columns: {list(row.keys())}")
        
        ustrd.text = "XYZ Bonus: " + str(invoice_id)
        
    except KeyError as e:
        print(f"Error processing row: {e}")
        raise

def convert_csv_to_xml(csv_file, output_xml):
    """Main conversion function"""
    try:
        # Load CSV data
        csv_data = load_csv(csv_file)
        
        if not csv_data:
            raise ValueError("CSV file is empty or could not be read")
        
        # Create base XML structure
        root = create_base_xml()
        
        # Process each row
        for i, row in enumerate(csv_data):
            try:
                add_transaction_to_xml(root, row)
            except Exception as e:
                print(f"Error processing row {i+1}: {e}")
                continue
        
        # Convert to pretty XML string
        xml_str = ET.tostring(root, encoding='unicode')
        pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent='    ')
        
        # Save to file
        with open(output_xml, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        return True
        
    except Exception as e:
        print(f"Conversion error: {e}")
        return False

class CSVToXMLConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("CSV to XML Converter")
        self.window.geometry("400x200")
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.window, text="CSV to XML Converter", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instruction_label = tk.Label(self.window, 
                                   text="Convert semicolon-separated CSV to XML format",
                                   font=("Arial", 10))
        instruction_label.pack(pady=5)
        
        # Convert button
        convert_button = tk.Button(self.window, text="Select CSV and Convert", 
                                 command=self.start_conversion,
                                 font=("Arial", 12),
                                 bg="#4CAF50", fg="white",
                                 padx=20, pady=10)
        convert_button.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(self.window, text="Ready to convert", 
                                   font=("Arial", 10))
        self.status_label.pack(pady=5)
        
    def start_conversion(self):
        try:
            # Select CSV file
            csv_file = filedialog.askopenfilename(
                title="Select CSV File", 
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not csv_file:
                return
            
            # Select output location
            output_xml = filedialog.asksaveasfilename(
                title="Save XML File As",
                defaultextension=".xml", 
                filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
            )
            
            if not output_xml:
                return
            
            # Update status
            self.status_label.config(text="Converting...")
            self.window.update()
            
            # Perform conversion
            success = convert_csv_to_xml(csv_file, output_xml)
            
            if success:
                self.status_label.config(text="Conversion completed successfully!")
                messagebox.showinfo("Success", 
                                  f"CSV successfully converted to XML!\nSaved as: {output_xml}")
            else:
                self.status_label.config(text="Conversion failed!")
                messagebox.showerror("Error", 
                                   "Conversion failed. Check console for details.")
                
        except Exception as e:
            self.status_label.config(text="Error occurred!")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"GUI Error: {e}")
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CSVToXMLConverter()
    app.run()
