import tkinter as tk
from tkinter import Event, messagebox, ttk
from typing import Any, cast

from src.core.di import Inject
from src.gui.modal.bank_account_form_modal import BankAccountFormModal
from src.gui.widget.context_menu import ContextMenu
from src.model.db_schema.bank_account_schema import BankAccountSchema
from src.model.design_pattern.creational_pattern.scrollable_tree_view_builder import (
    ScrollableTreeViewBuilder,
    ScrollableTreeViewDirector,
)
from src.model.bank_account_search import BankAccountSearch
from src.service.bank_account_service import BankAccountService

from src.exception.service_exception import ServiceException


class BankAccountScreen(ttk.Frame):
    __service: BankAccountService = cast(
        BankAccountService, Inject(BankAccountService)
    )

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill='both', expand=True)

        search_frame = ttk.Frame(master=self)
        self.iban_search_entry = ttk.Entry(master=search_frame)
        self.iban_search_entry.grid(column=0, row=0)
        search_button = ttk.Button(master=search_frame, text='Search', command=self._search_bank_accounts)
        search_button.grid(column=1, row=0)
        search_frame.pack(anchor='ne')

        # Define columns
        scrollableTreeViewDirrector = ScrollableTreeViewDirector(
            ScrollableTreeViewBuilder(master=self, columns=('id', 'iban'))
        )
        bindings = [('<Button-3>', self.on_right_click, False)]
        self.table = scrollableTreeViewDirrector.build_selectable_tree_view(
            bindings=bindings
        )

        self._search_bank_accounts()
        self.contextMenu = None

    def _identify_table_row(self, y: int) -> str:
        return self.table.tree_view.identify_row(y)

    def _edit_table_row(self, item: tuple[Any, ...]):
        data = BankAccountSchema(id=item[0], iban=item[1])
        BankAccountFormModal(master=self, model=data)
        self.table.tree_view.item(item[0], values=(data.id, data.iban))

    def _delete_table_row(self, item: tuple[Any, ...]):
        try:
            if messagebox.askyesno(
                title='Delete Confirmation',
                message='Are you sure you want to delete this bank account?',
                icon='warning',
            ):
                self.__service.delete_bank_account(item[0])
                self.table.tree_view.delete(item[0])
        except ServiceException as e:
            messagebox.showerror('Error', f'Failed to delete bank account:\n{str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'An unexpected error occurred while deleting bank account:\n{str(e)}')
        
    def on_right_click(self, event: Event):
        if self.contextMenu is not None:
            self.contextMenu.destroy()
            self.contextMenu = None

        item_id = self._identify_table_row(event.y)
        if item_id:
            self.table.tree_view.selection_set([item_id])
            selected_item = self.table.tree_view.item(item_id, 'values')
            commands = [
                ('Create new bank account', lambda: BankAccountFormModal(), True),
                ('Edit item', lambda: self._edit_table_row(selected_item), False),
                ('Delete item', lambda: self._delete_table_row(selected_item), False),
            ]
            self.contextMenu = ContextMenu(master=self, commands=commands)
            self.contextMenu.show_menu(event=event)

    def _search_bank_accounts(self):
        try:
            search_model = BankAccountSearch(iban=self.iban_search_entry.get())
            results = self.__service.search_bank_account(search_model)
            # Clear existing data
            for item in self.table.tree_view.get_children():
                self.table.tree_view.delete(item)
            # Insert new data
            for item in results:
                self.table.tree_view.insert(
                    parent='', index=tk.END, iid=item.id, values=(item.id, item.iban)
                )
        except ServiceException as e:
            messagebox.showerror('Error', f'Failed to search bank accounts:\n{str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'An unexpected error occurred while searching bank accounts:\n{str(e)}')
