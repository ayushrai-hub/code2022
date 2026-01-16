    # ------------------------------------------------------------------
    #  Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _row_hash(row_as_list: list) -> str:
        """
        Md5 hash of the full row so we can detect duplicates
        independently from the input file.
        """
        joined = "§".join([str(x) for x in row_as_list])  # unlikely splitter
        return hashlib.md5(joined.encode("utf‑8")).hexdigest()

    @staticmethod
    def _only_date(value: str) -> str:
        """
        Extracts only the yyyy-mm-dd part from a string that may contain
        both date and time.  If it already looks like a date it is
        returned unchanged.
        """
        try:
            return str(pd.to_datetime(value).date())
        except Exception:
            return ""

    # ------------------------------------------------------------------
    #  Pattern detection
    # ------------------------------------------------------------------
    def detect_bank_pattern(self, row_as_list: list) -> str | None:
        """
        Returns one of
            'BankOne Credit', 'BankOne Debit',
            'BankTwo Credit', 'BankTwo Debit'
        or None if the line does not match any known layout.
        The heuristics below are tailored to the two example banks
        (they can of course be refined later).
        """

        ln = len(row_as_list)

        # -----------------  BankOne  -----------------------------------
        # BankOne  Credit : 3 columns  [DatePurchased, Amount, Explanation]
        # BankOne  Debit  : 4 columns  [DateProcessed, Amount, Explanation, Balance]
        if ln in (3, 4):
            if pd.api.types.is_datetime64_any_dtype(pd.to_datetime(row_as_list[0], errors="coerce")):
                if ln == 3:
                    return "BankOne Credit"
                else:
                    return "BankOne Debit"

        # -----------------  BankTwo  -----------------------------------
        # BankTwo Credit : 4 columns  [blank, Explanation, Amount, DatePurchased]
        # BankTwo Debit  : 4 columns  [Balance, Explanation, Amount, DateProcessed]
        if ln == 4:
            # Credit – first column empty (or NaN) and last column is a date
            if (pd.isna(row_as_list[0]) or str(row_as_list[0]).strip() == "") and \
               pd.to_datetime(row_as_list[3], errors="coerce") is not pd.NaT:
                return "BankTwo Credit"

            # Debit – first column is a number (balance) and last column is a date
            if pd.to_numeric(row_as_list[0], errors="coerce") is not pd.NA and \
               pd.to_datetime(row_as_list[3], errors="coerce") is not pd.NaT:
                return "BankTwo Debit"

        return None

    # ------------------------------------------------------------------
    #  Record builder
    # ------------------------------------------------------------------
    def _build_record(self, pattern: str, row: list) -> dict:
        """
        Converts one CSV row into the standard database layout
        according to the mapping rules given in the specification.
        """

        # Default empty record
        rec = {col: "" for col in self.database_df.columns}

        if pattern == "BankOne Credit":
            rec.update({
                "Record":            ",".join(map(str, row)),
                "Date Purchased":    row[0],
                "Amount":            row[1],
                "Explanation":       row[2],
                "Type":              "CreditCard",
                "BANK":             "BankOne",
            })

        elif pattern == "BankOne Debit":
            rec.update({
                "Record":            ",".join(map(str, row)),
                "Date Processed":    row[0],
                "Amount":            row[1],
                "Explanation":       row[2],
                "Balance":           row[3],
                "Date Purchased":    self._only_date(row[2]),
                "Type":              "DebitCard",
                "BANK":             "BankOne",
            })

        elif pattern == "BankTwo Credit":
            rec.update({
                "Record":            ",".join(map(str, row)),
                "Date Purchased":    row[3],
                "Amount":            row[2],
                "Explanation":       row[1],
                "Type":              "CreditCard",
                "BANK":             "BankTwo",
            })

        elif pattern == "BankTwo Debit":
            rec.update({
                "Record":            ",".join(map(str, row)),
                "Balance":           row[0],
                "Explanation":       row[1],
                "Amount":            row[2],
                "Date Processed":    row[3],
                "Date Purchased":    self._only_date(row[1]),
                "Type":              "DebitCard",
                "BANK":             "BankTwo",
            })

        return rec

    # ------------------------------------------------------------------
    #  Main import routine
    # ------------------------------------------------------------------
    def load_records(self):
        """
        Lets the user pick a CSV file, recognises each row,
        de‑duplicates on md5 hash and stores new rows in the database.
        """

        fp = filedialog.askopenfilename(
            title="Select a bank record file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if not fp:
            return

        try:
            incoming_df = pd.read_csv(fp, header=None).fillna('')
        except Exception as exc:
            messagebox.showerror("Error", f"Cannot read file:\n{exc}")
            return

        new_rows = []
        duplicates = 0

        for _, r in incoming_df.iterrows():
            row_list = r.tolist()
            pattern   = self.detect_bank_pattern(row_list)

            if not pattern:
                # Skip unknown layouts – could also raise an error or log
                continue

            row_hash = self._row_hash(row_list)

            # Duplicate?  (ID column keeps the hashes)
            if row_hash in set(self.database_df["ID"]):
                duplicates += 1
                continue     # already stored – skip

            # Build and append the brand‑new record
            rec = self._build_record(pattern, row_list)
            rec["ID"] = row_hash
            new_rows.append(rec)

        # Persist if we actually imported something
        if new_rows:
            self.database_df = pd.concat(
                [self.database_df, pd.DataFrame(new_rows)],
                ignore_index=True
            )
            self.database_df.to_csv(self.database_filename, index=False)

        self.refresh_tree_view()

        # Feedback to the user
        messagebox.showinfo(
            "Import finished",
            f"Imported: {len(new_rows)}  |  Duplicates skipped: {duplicates}"
        )
