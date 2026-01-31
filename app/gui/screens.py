import app.gui.widgets as widgets
import tkinter as tk


class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.__setup_widgets()
    
    def __setup_widgets(self):
        label = tk.Label(self, text="Welcome to pyExpenses!", font=("Arial", 18))
        label.pack(pady=20)


class BankAccountScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.__setup_widgets()

    def __setup_widgets(self):
        search_frame = tk.Frame(master=self)
        iban_search_entry = tk.Entry(master=search_frame)
        iban_search_entry.grid(column=0, row=0)
        search_button = tk.Button(master=search_frame, text="Search")
        search_button.grid(column=1, row=0)
        search_frame.pack(anchor="ne")
        
        # Define columns
        columns = ("id","iban",)
        table = widgets.ScrollableTreeView(self, columns=columns, show="headings")
        table.pack(side=tk.LEFT, fill="both", expand=True)

        # Configure the headers (what appears on top)
        for column in columns:
            table.tree_view.heading(column=column, text=column.capitalize())
            table.tree_view.column(column=column, stretch=True)

        # Insert data
        data = [(x, "PT50" + str(x) * 28) for x in range(1, 501)]
        for item in data:
            table.tree_view.insert(parent="",index=tk.END,values=item)
        