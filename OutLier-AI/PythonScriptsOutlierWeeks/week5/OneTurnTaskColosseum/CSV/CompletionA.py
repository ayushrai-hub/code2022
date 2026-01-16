import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os

# -------------- CONFIGURE YOUR COLUMN NAMES HERE ---------------
COL_DEBTOR      = "debtor number"
COL_PRICE       = "Total Price"
COL_OWNER       = "account owner"
COL_IBAN        = "Iban"
COL_INVOICE     = "Invoice Id"
# ---------------------------------------------------------------

def load_csv(csv_path: str):
    """
    Reads a semicolon separated CSV and returns a list[dict]
    """
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh, delimiter=';')
        rows = list(reader)

    # Debug helper – print headers found
    print("Headers detected:", reader.fieldnames)
    return rows, reader.fieldnames


def build_xml(rows):
    """
    Builds the required XML tree from csv rows.
    Returns a pretty‑printed xml string.
    """

    # Root element – change the tag to your real template root if needed
    root = ET.Element("Document")

    for r in rows:
        try:
            debtor      = r[COL_DEBTOR].strip()
            price       = r[COL_PRICE].replace('€', '').replace('$', '').replace(',', '.').strip()
            owner       = r[COL_OWNER].strip()
            iban        = r[COL_IBAN].strip()
            invoice     = r[COL_INVOICE].strip()
        except KeyError as ke:
            raise KeyError(
                f"Column {ke!s} not found in CSV.\n\n"
                f"Found columns: {list(r.keys())}"
            )

        # <CdtTrfTxInf>
        cdt = ET.SubElement(root, "CdtTrfTxInf")

        # <PmtId><EndToEndId>
        pmt_id = ET.SubElement(cdt, "PmtId")
        ET.SubElement(pmt_id, "EndToEndId").text = f"XYZ {debtor}"

        # <Amt><InstdAmt Ccy="EUR">
        amt = ET.SubElement(cdt, "Amt")
        ET.SubElement(amt, "InstdAmt", Ccy="EUR").text = price

        # <Cdtr><Nm>
        cdtr = ET.SubElement(cdt, "Cdtr")
        ET.SubElement(cdtr, "Nm").text = owner

        # <CdtrAcct><Id>
        cdtr_acct = ET.SubElement(cdt, "CdtrAcct")
        ET.SubElement(cdtr_acct, "Id").text = iban

        # <RmtInf><Ustrd>
        rmt = ET.SubElement(cdt, "RmtInf")
        ET.SubElement(rmt, "Ustrd").text = f"XYZ Bonus: {invoice}"

    # Pretty print
    rough = ET.tostring(root, encoding='utf-8')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ")


def convert(csv_path, out_path):
    rows, headers = load_csv(csv_path)

    try:
        xml_text = build_xml(rows)
    except KeyError as e:
        messagebox.showerror("Missing column", str(e))
        return

    with open(out_path, "w", encoding='utf-8') as fh:
        fh.write(xml_text)

    messagebox.showinfo("Success", f"XML written to:\n{os.path.abspath(out_path)}")


# ------------------------- GUI ---------------------------------
def gui():
    root = tk.Tk()
    root.title("CSV ➜ XML converter")

    def run():
        csv_path = filedialog.askopenfilename(
            title="Choose CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not csv_path:
            return

        out_path = filedialog.asksaveasfilename(
            defaultextension=".xml",
            filetypes=[("XML files", "*.xml")]
        )
        if not out_path:
            return

        convert(csv_path, out_path)

    tk.Button(root, text="Convert CSV to XML", width=30, command=run).pack(padx=20, pady=20)
    root.mainloop()


if __name__ == "__main__":
    gui()
