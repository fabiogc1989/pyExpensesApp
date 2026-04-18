import tkinter as tk 
from tkinter import ttk

from src.core.di import Inject
from src.model.design_pattern.creational_pattern.scrollable_tree_view_builder import ScrollableTreeViewBuilder, ScrollableTreeViewDirector
from src.repository.transaction_view_repository import TransactionViewRepository
from src.service.transaction_service import TransactionService


class ViewTransactionsScreen(ttk.Frame):
    __service: TransactionService = Inject(TransactionService)

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        scrollableTreeViewDirrector = ScrollableTreeViewDirector(ScrollableTreeViewBuilder(master=self, columns=('Transaction ID', 'Description', 'Amount', 'Date', 'Type', 'IBAN')))
        self.table = scrollableTreeViewDirrector.build_standard_tree_view()

        # Insert data
        data = self.__service.search_transactions()
        for item in data:
            self.table.tree_view.insert(parent="",index=tk.END, iid=item.row_number, values=(item.transaction_id, item.description, item.amount, item.date, item.type.name, item.iban))
        