import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from tkinter import messagebox
from datetime import datetime

class MyApp(tk.Tk):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.title("Financial Transactions Viewer")
        self.geometry("1300x600")
        self.flat_categories = [] 
        self.current_view = "data"  # Track current view

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

        self.style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'), background=classic_bg)

        self.style.configure("TButton", font=('Calibri', 10, 'bold'), background=btn_bg, foreground=btn_fg)

        self.style.configure("TCombobox", fieldbackground=treeview_field_bg, background="white")

        self.create_widgets()
        self.show_data_view()  # Start with data view

    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # SHARED WIDGETS (visible in both views)
        self.create_shared_widgets()
        
        # DATA VIEW WIDGETS
        self.create_data_widgets()
        
        # GRAPH VIEW WIDGETS
        self.create_graph_widgets()

    def create_shared_widgets(self):
        """Create widgets that are shared between both views"""
        self.shared_frame = ttk.Frame(self.main_frame)
        self.shared_frame.pack(fill=tk.X)

        # Button frame with both buttons
        self.button_frame = ttk.Frame(self.shared_frame)
        self.button_frame.pack(pady=10, fill=tk.X)

        self.load_button = ttk.Button(self.button_frame, text="Import Transaction Records", 
                                     command=self.load_records, style="TButton")
        self.load_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.show_graph_button = ttk.Button(self.button_frame, text="Show Graph", 
                                           command=self.show_graph_view, style="TButton")
        self.show_graph_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        # Horizontal separator
        self.separator = ttk.Separator(self.shared_frame, orient='horizontal')
        self.separator.pack(fill='x', padx=2, pady=2)

    def create_data_widgets(self):
        """Create widgets specific to the Data view"""
        self.data_frame = ttk.Frame(self.main_frame)
        
        # Search frame
        self.search_frame = ttk.Frame(self.data_frame)
        self.search_frame.pack(pady=10, fill=tk.X)

        self.search_var = tk.StringVar()
        self.search_box = ttk.Entry(self.search_frame, textvariable=self.search_var, width=50)
        self.search_box.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.search_box.insert(0, "Search Transactions...")
        self.search_box.bind("<FocusIn>", lambda args: self.search_box.delete('0', 'end') if self.search_var.get() == "Search Transactions..." else None)
        self.search_box.bind("<FocusOut>", lambda args: self.search_box.insert(0, "Search Transactions...") if not self.search_var.get() else None)

        self.uncategorized_var = tk.BooleanVar()
        self.uncategorized_check = ttk.Checkbutton(self.search_frame, text="Uncategorized Only", variable=self.uncategorized_var)
        self.uncategorized_check.grid(row=0, column=1, sticky="w")

        # Treeview
        self.tree = ttk.Treeview(self.data_frame, columns=("Transaction", "Purchase Date", "Post Date", "Amount", "Details", "Balance"), 
                                show="headings", style="Treeview")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Category selection
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(self.data_frame, textvariable=self.category_var, style="TCombobox")
        self.category_combobox.pack(pady=2, fill=tk.X)
        self.category_combobox.bind('<KeyRelease>', self.filter_category_options)

        self.categorize_button = ttk.Button(self.data_frame, text="Assign Category", style="TButton")
        self.categorize_button.pack(pady=2, fill=tk.X)

    def create_graph_widgets(self):
        """Create widgets specific to the Graph view"""
        self.graph_frame = ttk.Frame(self.main_frame)
        
        # Placeholder for graph interface
        self.graph_title = ttk.Label(self.graph_frame, text="Graph View", font=('Calibri', 16, 'bold'))
        self.graph_title.pack(pady=20)
        
        self.graph_placeholder = ttk.Label(self.graph_frame, text="Graph visualization will be displayed here", 
                                          font=('Calibri', 12))
        self.graph_placeholder.pack(pady=10)
        
        # Button to return to data view
        self.show_data_button = ttk.Button(self.graph_frame, text="Show Data", 
                                          command=self.show_data_view, style="TButton")
        self.show_data_button.pack(pady=20, fill=tk.X)

    def show_data_view(self):
        """Show the Data interface and hide Graph interface"""
        if self.current_view != "data":
            self.graph_frame.pack_forget()
            self.data_frame.pack(fill=tk.BOTH, expand=True)
            self.current_view = "data"
            self.show_graph_button.config(text="Show Graph", command=self.show_graph_view)

    def show_graph_view(self):
        """Show the Graph interface and hide Data interface"""
        if self.current_view != "graph":
            self.data_frame.pack_forget()
            self.graph_frame.pack(fill=tk.BOTH, expand=True)
            self.current_view = "graph"
            self.show_graph_button.config(text="Show Data", command=self.show_data_view)

    def read_categories(self, filepath):
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            headers = df.columns.tolist()
            categories = {header: [] for header in headers}
            for index, row in df.iterrows():
                for header in headers:
                    item = row[header]
                    if pd.notnull(item):
                        categories[header].append(item)
            self.flat_categories = [f"{header} > {item}" for header, items in categories.items() for item in items]

    def filter_category_options(self, event=None):
        current_input = self.category_var.get().lower()
        filtered_options = []
        for option in self.flat_categories:
            try:
                category, sub_category = option.split(" > ", 1)
            except ValueError:
                continue
            if current_input in sub_category.lower():
                filtered_options.append(option)
        self.category_combobox['values'] = filtered_options
        if current_input and filtered_options:
            self.category_combobox.event_generate('<Down>')

    def load_records(self):
        filepath = './database.csv'
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            if not df.empty and len(df.columns) >= 8:
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                total_records = len(df)
                unassigned_records = len(df[df['Entity'].isnull()])
                messagebox.showinfo("Information", f"The file you were working on was last saved on {mod_time} and contains {total_records} records, with {unassigned_records} (%) uncategorized.")
                for _, row in df.iterrows():
                    self.tree.insert("", "end", values=(row['Transaction'], row['Purchase Date'], row['Post Date'], row['Amount'], row['Details'], row['Balance']))
            else:
                messagebox.showwarning("Warning", "The CSV file is either empty or lacks the necessary columns.")
        else:
            messagebox.showerror("Error", "Database file could not be located.")

def main():
    app = MyApp()
    app.read_categories('./categories.csv')
    app.mainloop()

if __name__ == "__main__":
    main()
