# ---------------------------------------------------------------------------
# 1.  NEW  – helper functions
# ---------------------------------------------------------------------------
def md5_line(line: list[str]) -> str:
    """Return the md5 of the *string* representation of an input row."""
    return hashlib.md5("||".join(map(str, line)).encode()).hexdigest()


def is_date(text: str) -> bool:                # (tiny helper that already existed
    try:                                       #  elsewhere in your project)
        datetime.datetime.strptime(text, "%d/%m/%Y")
        return True
    except Exception:
        return False
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 2.  MODIFIED  – detect_bank_pattern()
# ---------------------------------------------------------------------------
def detect_bank_pattern(self, row: list):
    """
    Return a string describing which template the current row matches or None.
    Expected return values:
        'MetroBank Credit' | 'MetroBank Debit' | 'HSBC Credit' | 'HSBC Debit'
    """
    if len(row) < 4:
        return None

    # ---- HSBC -------------------------------------------------------------
    if (is_date(str(row[3])) and pd.api.types.is_number(row[2])
            and isinstance(row[1], str)):
        if pd.isna(row[0]):
            return "HSBC Credit"
        if pd.api.types.is_number(row[0]):
            return "HSBC Debit"

    # ---- MetroBank --------------------------------------------------------
    # MetroBank exports always start with a date in column‑0
    if is_date(str(row[0])) and isinstance(row[2], str):
        # Credit‑card files contain 3 columns only
        if len(row) == 3:
            return "MetroBank Credit"
        # Debit card has 4 columns (balance in column‑3)
        if len(row) >= 4 and pd.api.types.is_number(row[3]):
            return "MetroBank Debit"

    return None
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 3.  NEW  – four dedicated processors
# ---------------------------------------------------------------------------
def process_metro_credit(self, row):
    _id = md5_line(row)
    if _id in self.database_df["ID"].values:
        return                                             # already stored

    new = {
        "Record":             " | ".join(map(str, row)),
        "Date Purchased":     row[0],
        "Figure":             row[1],
        "Description":        row[2],
        "Type":               "CreditCard",
        "ID":                 _id,
        "BANK":               "MetroBank"
    }
    self.database_df.loc[len(self.database_df)] = new


def process_metro_debit(self, row):
    _id = md5_line(row)
    if _id in self.database_df["ID"].values:
        return

    # derive purchase‑date from Description column (col‑2)
    date_purchased = None
    for token in str(row[2]).split():
        if is_date(token):
            date_purchased = token
            break

    new = {
        "Record":          " | ".join(map(str, row)),
        "Date Committed":  row[0],
        "Figure":          row[1],
        "Description":     row[2],
        "Balance":         row[3],
        "Date Purchased":  date_purchased,
        "Type":            "DebitCard",
        "ID":              _id,
        "BANK":            "MetroBank"
    }
    self.database_df.loc[len(self.database_df)] = new


def process_hsbc_credit(self, row):
    _id = md5_line(row)
    if _id in self.database_df["ID"].values:
        return

    new = {
        "Record":          " | ".join(map(str, row)),
        "Date Purchased":  row[3],
        "Figure":          row[2],
        "Description":     row[1],
        "Type":            "CreditCard",
        "ID":              _id,
        "BANK":            "HSBC"
    }
    self.database_df.loc[len(self.database_df)] = new


def process_hsbc_debit(self, row):
    _id = md5_line(row)
    if _id in self.database_df["ID"].values:
        return

    # derive purchase‑date from Description column (col‑1)
    date_purchased = None
    for token in str(row[1]).split():
        if is_date(token):
            date_purchased = token
            break

    new = {
        "Record":          " | ".join(map(str, row)),
        "Balance":         row[0],
        "Description":     row[1],
        "Figure":          row[2],
        "Date Committed":  row[3],
        "Date Purchased":  date_purchased,
        "Type":            "DebitCard",
        "ID":              _id,
        "BANK":            "HSBC"
    }
    self.database_df.loc[len(self.database_df)] = new
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 4.  MODIFIED  – load_records(): now calls the correct processor
# ---------------------------------------------------------------------------
for index, row in input_df.iterrows():
    row_list = row.tolist()
    pattern = self.detect_bank_pattern(row_list)

    if pattern == "MetroBank Credit":
        self.process_metro_credit(row_list)
    elif pattern == "MetroBank Debit":
        self.process_metro_debit(row_list)
    elif pattern == "HSBC Credit":
        self.process_hsbc_credit(row_list)
    elif pattern == "HSBC Debit":
        self.process_hsbc_debit(row_list)
    else:
        print(f"Row {index} does not match any expected pattern – skipped.")
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 5.  MODIFIED  – end of load_records(): save & refresh
# ---------------------------------------------------------------------------
self.database_df.to_csv(self.database_filename, index=False)
self.refresh_tree_view()
print("File processing completed.")
# ---------------------------------------------------------------------------
