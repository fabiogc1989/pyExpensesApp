from src.gui.modal.bank_account_form_modal import BankAccountFormModal
import src.gui.widgets as widgets
import tkinter as tk
from tkinter import ttk, Event, messagebox
from src.models.database_schema import BankAccountSchema
from src.repositories.bank_account_repository import BankAccountRepository


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
        self.table.bind('<Button-3>', self.on_right_click)

        self.table.pack(side=tk.LEFT, fill="both", expand=True)

        # Configure the headers (what appears on top)
        for column in columns:
            self.table.tree_view.heading(column=column, text=column.capitalize())
            self.table.tree_view.column(column=column, stretch=True)

        # Insert data
        data = self.repository.get_all()
        for item in data:
            self.table.tree_view.insert(parent="",index=tk.END, iid=item.id, values=(item.id, item.iban))
        
        self.contextMenu = None

    def _identify_table_row(self, y: int) -> str:
        return self.table.tree_view.identify_row(y)
    
    def _edit_table_row(self, item: tuple[any, ...]):
        data = BankAccountSchema(id=item[0], iban=item[1])
        BankAccountFormModal(master=self, model=data)
        self.table.tree_view.item(item[0], values=(data.id, data.iban))
    
    def _delete_table_row(self, item: tuple[any, ...]):
        if messagebox.askyesno(title='Delete Confirmation', message='Are you sure you want to delete this bank account?', icon='warning'):
            self.repository.delete(item[0])
            self.table.tree_view.delete(item[0])

    def on_right_click(self, event: Event):
        if self.contextMenu is not None:
            self.contextMenu.destroy()
            self.contextMenu = None

        item_id = self._identify_table_row(event.y)
        if item_id:
            self.table.tree_view.selection_set([item_id])
            selected_item = self.table.tree_view.item(item_id, 'values')
            commands=[('Edit', lambda: self._edit_table_row(selected_item)), ('Delete', lambda: self._delete_table_row(selected_item))]
            self.contextMenu = widgets.ContextMenu(master=self, commands=commands)
            self.contextMenu.show_menu(event=event)