import tkinter as tk
from tkinter import ttk


class ScrollableTreeView(tk.Frame):
    def __init__(self, master, columns, *args, **kwargs):
        super().__init__(master)

        self._treeview = ttk.Treeview(master, columns=columns, *args, **kwargs)

        # Create scrollbars
        self.vertical_scrollbar = ttk.Scrollbar(master=self._treeview, orient=tk.VERTICAL, command=self._treeview.yview)
        self.horizontal_scrollbar = ttk.Scrollbar(master=self._treeview, orient=tk.HORIZONTAL, command=self._treeview.xview)
        # Configure the Treeview to use the scrollbars
        self._treeview.configure(yscrollcommand=self.vertical_scrollbar.set, xscrollcommand=self.horizontal_scrollbar.set)
        # Pack the scrollbars
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._treeview.pack(side=tk.LEFT, fill="both", expand=True)
    
    @property
    def tree_view(self):
        return self._treeview