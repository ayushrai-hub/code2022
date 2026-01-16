import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from tkinter import messagebox
from datetime import datetime


class MyApp(tk.Tk):
    # ------------------------------------------------------------------ INIT
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title("Financial Transactions Viewer")
        self.geometry("1300x600")
        self.flat_categories = []

        # ------------------------------ STYLES
        self._init_styles()

        # ------------------------------ GUI
        self._create_containers()
        self._create_shared_widgets()
        self._create_data_widgets()
        self._create_graph_widgets()

        #  Show Data view first
        self.show_data()

    # ================================================================ GUI ===
    # ---------------------------------------------------------------- STYLES
    def _init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        classic_bg = "#F5F5F5"
        btn_bg = "#D3D3D3"
        btn_fg = "maroon"
        treeview_bg = "#FFFFFF"
        treeview_field_bg = "#F5F5F5"
        selected_bg = "#C0C0C0"

        self.style.configure("Treeview", background=treeview_bg, foreground="black",
                             rowheight=25, fieldbackground=treeview_field_bg)
        self.style.map("Treeview", background=[('selected', selected_bg)])
        self.style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'),
                             background=classic_bg)
        self.style.configure("TButton", font=('Calibri', 10, 'bold'),
                             background=btn_bg, foreground=btn_fg)
        self.style.configure("TCombobox", fieldbackground=treeview_field_bg,
                             background="white")

    # ----------------------------------------------------------- CONTAINERS
    def _create_containers(self):
        """Create the three main frames:
           - shared_frame : widgets visible on both views
           - data_frame   : widgets visible only on the Data view
           - graph_frame  : widgets visible only on the Graph view
        """
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.shared_frame = ttk.Frame(self.main_frame)
        self.shared_frame.pack(fill=tk.X)           # always visible

        # view‑specific frames – start stacked, visibility controlled later
        self.data_frame = ttk.Frame(self.main_frame)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = ttk.Frame(self.main_frame)
        self.graph_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # same size
        # graph_frame will be raised / lowered by show_graph() / show_data()

    # ----------------------------------------------------------- SHARED WDG
    def _create_shared_widgets(self):
        # Top‑row buttons
        button_frame = ttk.Frame(self.shared_frame)
        button_frame.pack(pady=10, fill=tk.X)

        load_button = ttk.Button(button_frame, text="Import Transaction Records",
                                 command=self.load_records, style="TButton")
        load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.show_graph_btn = ttk.Button(button_frame, text="Show Graph",
                                         command=self.show_graph, style="TButton")
        self.show_graph_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Horizontal separator (shared)
        separator = ttk.Separator(self.shared_frame, orient='horizontal')
        separator.pack(fill='x', padx=2, pady=2)

    # -------------------------------------------------------------- DATA WDG
    def _create_data_widgets(self):
        """Widgets only relevant to the Data interface."""
        # ---- Search line
        search_frame = ttk.Frame(self.data_frame)
        search_frame.pack(pady=10, fill=tk.X)

        self.search_var = tk.StringVar()
        search_box = ttk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_box.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        search_box.insert(0, "Search Transactions...")
        search_box.bind("<FocusIn>",
                        lambda _=None: search_box.delete('0', 'end')
                        if self.search_var.get() == "Search Transactions..." else None)
        search_box.bind("<FocusOut>",
                        lambda _=None: search_box.insert(0, "Search Transactions...")
                        if not self.search_var.get() else None)

        self.uncategorized_var = tk.BooleanVar()
        uncategorized_check = ttk.Checkbutton(search_frame,
                                              text="Uncategorized Only",
                                              variable=self.uncategorized_var)
        uncategorized_check.grid(row=0, column=1, sticky="w")

        # ---- Treeview
        self.tree = ttk.Treeview(self.data_frame,
                                 columns=("Transaction", "Purchase Date",
                                          "Post Date", "Amount", "Details",
                                          "Balance"),
                                 show="headings", style="Treeview")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # ---- Category combobox + button
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.data_frame,
                                              textvariable=self.category_var,
                                              style="TCombobox")
        self.category_combobox.pack(pady=2, fill=tk.X)
        self.category_combobox.bind('<KeyRelease>', self.filter_category_options)

        categorize_button = ttk.Button(self.data_frame, text="Assign Category",
                                       style="TButton")
        categorize_button.pack(pady=2, fill=tk.X)

    # ------------------------------------------------------------- GRAPH WDG
    def _create_graph_widgets(self):
        """Stub widgets for the Graph interface."""
        lbl = ttk.Label(self.graph_frame, text="Graph view goes here",
                        font=("Calibri", 16, "bold"))
        lbl.place(relx=0.5, rely=0.5, anchor="center")

        # Button to return to data view
        back_btn = ttk.Button(self.graph_frame, text="Back to Data",
                              command=self.show_data, style="TButton")
        back_btn.place(relx=0.5, rely=0.6, anchor="center")

    # ========================================================= VIEW SWITCH
    def show_graph(self):
        """Display graph widgets, hide data widgets."""
        self.graph_frame.lift()         # bring graph frame to front

    def show_data(self):
        """Display data widgets, hide graph widgets."""
        self.data_frame.lift()          # bring data frame to front

    # ========================================================== FUNCTIONS ==
    # ----------------------------------------------------------------- CAT
    def read_categories(self, filepath):
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            headers = df.columns.tolist()
            categories = {header: [] for header in headers}
            for _, row in df.iterrows():
                for header in headers:
                    item = row[header]
                    if pd.notnull(item):
                        categories[header].append(item)
            self.flat_categories = [f"{header} > {item}"
                                    for header, items in categories.items()
                                    for item in items]

    def filter_category_options(self, event=None):
        current_input = self.category_var.get().lower()
        filtered_options = []
        for option in self.flat_categories:
            try:
                _, sub_category = option.split(" > ", 1)
            except ValueError:
                continue
            if current_input in sub_category.lower():
                filtered_options.append(option)
        self.category_combobox['values'] = filtered_options
        if current_input and filtered_options:
            self.category_combobox.event_generate('<Down>')

    # ---------------------------------------------------------------- LOAD
    def load_records(self):
        filepath = './database.csv'
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            if not df.empty and len(df.columns) >= 8:
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)) \
                    .strftime('%Y-%m-%d %H:%M:%S')
                total_records = len(df)
                unassigned_records = len(df[df['Entity'].isnull()])
                messagebox.showinfo(
                    "Information",
                    f"The file you were working on was last saved on "
                    f"{mod_time} and contains {total_records} records, with "
                    f"{unassigned_records} (%) uncategorized.")
                for _, row in df.iterrows():
                    self.tree.insert("", "end",
                                     values=(row['Transaction'],
                                             row['Purchase Date'],
                                             row['Post Date'],
                                             row['Amount'],
                                             row['Details'],
                                             row['Balance']))
            else:
                messagebox.showwarning(
                    "Warning",
                    "The CSV file is either empty or lacks the necessary columns.")
        else:
            messagebox.showerror("Error", "Database file could not be located.")


# ================================================================== MAIN ==
def main():
    app = MyApp()
    app.read_categories('./categories.csv')
    app.mainloop()


if __name__ == "__main__":
    main()
