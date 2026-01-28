import tkinter as tk
from tkinter import ttk
import app.gui.widgets as widgets


class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        label = ttk.Label(self, text="Welcome to pyExpenses!", font=("Arial", 18))
        label.pack(pady=20)


class BankAccountScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        # Define columns
        columns = ("id","iban",)

        table = widgets.ScrollableTreeView(self, columns=columns, show="headings")

        # Configure the headers (what appears on top)
        for column in columns:
            table.tree_view.heading(column=column, text=column.capitalize())
            table.tree_view.column(column=column, stretch=True)

        # Insert data
        data = [(x, "PT50" + str(x) * 28) for x in range(1, 501)]
        for item in data:
            table.tree_view.insert(parent="",index=tk.END,values=item)
