import tkinter as tk 
from tkinter import ttk

from src.model.design_pattern.creational_pattern.scrollable_tree_view_builder import ScrollableTreeViewBuilder, ScrollableTreeViewDirector


class ViewTransactionsScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        scrollableTreeViewDirrector = ScrollableTreeViewDirector(ScrollableTreeViewBuilder(master=self, columns=('id', 'description', 'amount', 'date', 'type', 'bank_account_id')))
        self.table = scrollableTreeViewDirrector.build_scrollable_tree_view(show='headings', selectmode='browse', fill='both', side=tk.LEFT, expand=True)