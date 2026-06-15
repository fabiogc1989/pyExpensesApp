import tkinter as tk
from tkinter import ttk
from typing import Any, Literal


class ScrollableTreeView(tk.Frame):
    def __init__(self, master, columns, *args, **kwargs):
        super().__init__(master)

        self.__treeview = ttk.Treeview(master, columns=columns, *args, **kwargs)

        # Create scrollbars
        self.__vertical_scrollbar = ttk.Scrollbar(
            master=self.__treeview, orient=tk.VERTICAL, command=self.__treeview.yview
        )
        self.__horizontal_scrollbar = ttk.Scrollbar(
            master=self.__treeview, orient=tk.HORIZONTAL, command=self.__treeview.xview
        )
        # Configure the Treeview to use the scrollbars
        self.__treeview.configure(
            yscrollcommand=self.__vertical_scrollbar.set,
            xscrollcommand=self.__horizontal_scrollbar.set,
        )

    @property
    def tree_view(self):
        return self.__treeview

    def pack(
        self,
        side: Literal['left', 'right', 'top', 'bottom'] = tk.LEFT,
        fill: Literal['none', 'x', 'y', 'both'] = 'both',
        expand=False,
        *args,
        **kwargs,
    ):
        self.__horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.__vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__treeview.pack(side=side, fill=fill, expand=expand, *args, **kwargs)

    def bind(self, *args: Any, **kwargs: Any) -> Any:
        return self.tree_view.bind(*args, **kwargs)
