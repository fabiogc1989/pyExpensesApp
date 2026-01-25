import tkinter as tk
from tkinter import ttk


class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        label = ttk.Label(self, text="Welcome to pyExpenses!", font=("Arial", 18))
        label.pack(pady=20)


class BankAccountScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Define columns
        columns = ("id","iban",)

        table = ttk.Treeview(self, columns=columns,show="headings")
        
        vertical_scrollbar = ttk.Scrollbar(master=table, orient=tk.VERTICAL, command=table.yview)
        horizontal_scrollbar = ttk.Scrollbar(master=table, orient=tk.HORIZONTAL, command=table.xview)

        table.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

        self.pack(fill="both", expand=True)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        table.pack(side=tk.LEFT, fill="both", expand=True)

        # Configure the headers (what appears on top)
        for column in columns:
            table.heading(column=column, text=column.capitalize())
            table.column(column=column, stretch=True)

        # Insert data
        data = [(x, "PT50" + str(x) * 28) for x in range(1, 501)]
        for item in data:
            table.insert(parent="",index=tk.END,values=item)
