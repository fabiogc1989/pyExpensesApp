import tkinter as tk 
from tkinter import ttk

from src.core.di import Inject
from src.model.design_pattern.creational_pattern.scrollable_tree_view_builder import ScrollableTreeViewBuilder, ScrollableTreeViewDirector
from src.repository.transaction_view_repository import TransactionViewRepository


class ViewTransactionsScreen(ttk.Frame):
    repository = Inject(TransactionViewRepository)

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        scrollableTreeViewDirrector = ScrollableTreeViewDirector(ScrollableTreeViewBuilder(master=self, columns=('id', 'description', 'amount', 'date', 'type', 'bank_account_id')))
        self.table = scrollableTreeViewDirrector.build_scrollable_tree_view(show='headings', selectmode='browse', fill='both', side=tk.LEFT, expand=True)

        # Insert data
        data = self.repository.get_all()
        for item in data:
            self.table.tree_view.insert(parent="",index=tk.END, iid=item.unique_row_id, values=(item.id, item.description, item.amount, item.date, item.type, item.bank_account_id))
        