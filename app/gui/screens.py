import app.gui.widgets as widgets
import tkinter as tk
from tkinter import ttk, Event
from repositories.bank_account_repository import BankAccountRepository


class StartScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        label = ttk.Label(self, text="Welcome to pyExpenses!", font=("Arial", 18))
        label.pack(pady=20)        


class BankAccountScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.repository = BankAccountRepository()
        self.pack(fill="both", expand=True)
        
        search_frame = ttk.Frame(master=self)
        iban_search_entry = ttk.Entry(master=search_frame)
        iban_search_entry.grid(column=0, row=0)
        search_button = ttk.Button(master=search_frame, text="Search")
        search_button.grid(column=1, row=0)
        search_frame.pack(anchor="ne")
        
        # Define columns
        columns = ("id","iban")
        self.table = widgets.ScrollableTreeView(self, columns=columns, show="headings", selectmode= "browse")
        
        # Bind events
        # Selection bind
        self.table.bind('<<TreeviewSelect>>', self.on_table_select)

        self.table.pack(side=tk.LEFT, fill="both", expand=True)

        # Configure the headers (what appears on top)
        for column in columns:
            self.table.tree_view.heading(column=column, text=column.capitalize())
            self.table.tree_view.column(column=column, stretch=True)

        # Insert data
        data = self.repository.get_all()
        for item in data:
            self.table.tree_view.insert(parent="",index=tk.END, iid=item.id, values=(item.id, item.iban))
        
    def on_table_select(self, event: Event):
        item_id = self.table.tree_view.selection()[0]
        values = self.table.tree_view.item(item_id, 'values')
        print(values)