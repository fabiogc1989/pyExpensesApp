import tkinter as tk
from typing import Callable, Literal

from src.gui.widget.scrollable_tree_view import ScrollableTreeView


class ScrollableTreeViewBuilder:
    def __init__(self, master, columns):
        self.master = master
        self.columns = columns
        self.treeview_options = {}
        self.pack_options = {
            "side": tk.LEFT,
            "fill": "both",
            "expand": False
        }
        self.bindings = []

    def with_treeview_option(self, key, value):
        """Set a Treeview option (show, selectmode, height, etc.)"""
        self.treeview_options[key] = value
        return self

    def with_show(self, value):
        """Set the show option (e.g., 'headings', 'tree', 'tree headings')"""
        self.treeview_options["show"] = value
        return self

    def with_selectmode(self, value):
        """Set the selectmode option (e.g., 'browse', 'extended', 'multiple')"""
        self.treeview_options["selectmode"] = value
        return self

    def with_height(self, height: int):
        """Set the height of the Treeview"""
        self.treeview_options["height"] = height
        return self

    def with_pack_side(self, side):
        """Set the pack side option"""
        self.pack_options["side"] = side
        return self

    def with_pack_fill(self, fill):
        """Set the pack fill option"""
        self.pack_options["fill"] = fill
        return self

    def with_pack_expand(self, expand: bool):
        """Set the pack expand option"""
        self.pack_options["expand"] = expand
        return self

    def with_pack_options(self, side=None, fill=None, expand=None, **kwargs):
        """Set multiple pack options at once"""
        if side is not None:
            self.pack_options["side"] = side
        if fill is not None:
            self.pack_options["fill"] = fill
        if expand is not None:
            self.pack_options["expand"] = expand
        self.pack_options.update(kwargs)
        return self

    def add_binding(self, sequence: str, func: Callable, add: bool | Literal['', '+'] | None = None):
        """Add an event binding"""
        self.bindings.append({"sequence": sequence, "func": func, "add": add})
        return self

    def build(self) -> ScrollableTreeView:
        """Build and return the ScrollableTreeView instance"""
        table = ScrollableTreeView(
            self.master,
            self.columns,
            **self.treeview_options
        )

        # Configure the headers (what appears on top)
        for column in self.columns:
            table.tree_view.heading(column=column, text=column.capitalize())
            table.tree_view.column(column=column, stretch=True)

        # Apply bindings
        for binding in self.bindings:
            table.bind(
                sequence=binding["sequence"],
                func=binding["func"],
                add=binding["add"]
            )

        # Pack the tree view with configured options
        pack_kwargs = {k: v for k, v in self.pack_options.items() if k in ["side", "fill", "expand"]}
        extra_pack_options = {k: v for k, v in self.pack_options.items() if k not in ["side", "fill", "expand"]}
        table.pack(**pack_kwargs, **extra_pack_options)

        return table


class ScrollableTreeViewDirector:
    def __init__(self, builder: ScrollableTreeViewBuilder):
        self._builder = builder

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def build_scrollable_tree_view(self, show: str, selectmode: str, fill: str, side: str, expand: bool, bindings: list[dict[str, Callable, bool]]) -> ScrollableTreeView:
        self._builder\
            .with_show(show)\
            .with_selectmode(selectmode)

        for binding in bindings:
            sequence, func, add = binding["sequence"], binding["func"], binding["add"]
            self._builder.add_binding(sequence, func, add)

        self._builder\
            .with_pack_side(side)\
            .with_pack_fill(fill)\
            .with_pack_expand(expand)

        return self._builder.build()
