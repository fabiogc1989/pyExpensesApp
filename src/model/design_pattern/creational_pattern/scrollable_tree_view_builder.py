import tkinter as tk
from typing import Callable, Literal

from src.gui.widget.scrollable_tree_view import ScrollableTreeView


class ScrollableTreeViewBuilder:
    def __init__(self, master, columns):
        self._master = master
        self._columns = columns
        self._treeview_options = {}
        self._pack_options = {'side': tk.LEFT, 'fill': 'both', 'expand': False}
        self._bindings = []

    def with_treeview_option(self, key, value):
        """Set a Treeview option (show, selectmode, height, etc.)"""
        self._treeview_options[key] = value
        return self

    def with_show(self, value):
        """Set the show option (e.g., 'headings', 'tree', 'tree headings')"""
        self._treeview_options['show'] = value
        return self

    def with_selectmode(self, value):
        """Set the selectmode option (e.g., 'browse', 'extended', 'multiple')"""
        self._treeview_options['selectmode'] = value
        return self

    def with_height(self, height: int):
        """Set the height of the Treeview"""
        self._treeview_options['height'] = height
        return self

    def with_pack_side(self, side):
        """Set the pack side option"""
        self._pack_options['side'] = side
        return self

    def with_pack_fill(self, fill):
        """Set the pack fill option"""
        self._pack_options['fill'] = fill
        return self

    def with_pack_expand(self, expand: bool):
        """Set the pack expand option"""
        self._pack_options['expand'] = expand
        return self

    def with_pack_options(self, side=None, fill=None, expand=None, **kwargs):
        """Set multiple pack options at once"""
        if side is not None:
            self._pack_options['side'] = side
        if fill is not None:
            self._pack_options['fill'] = fill
        if expand is not None:
            self._pack_options['expand'] = expand
        self._pack_options.update(kwargs)
        return self

    def add_binding(
        self, sequence: str, func: Callable, add: bool | Literal['', '+'] | None = None
    ):
        """Add an event binding"""
        self._bindings.append({'sequence': sequence, 'func': func, 'add': add})
        return self

    def build(self) -> ScrollableTreeView:
        """Build and return the ScrollableTreeView instance"""
        table = ScrollableTreeView(self._master, self._columns, **self._treeview_options)

        # Configure the headers (what appears on top)
        for column in self._columns:
            table.tree_view.heading(column=column, text=column.capitalize())
            table.tree_view.column(column=column, stretch=True)

        # Apply bindings
        for binding in self._bindings:
            table.bind(
                sequence=binding['sequence'], func=binding['func'], add=binding['add']
            )

        # Pack the tree view with configured options
        pack_kwargs = {
            k: v for k, v in self._pack_options.items() if k in ['side', 'fill', 'expand']
        }
        extra_pack_options = {
            k: v
            for k, v in self._pack_options.items()
            if k not in ['side', 'fill', 'expand']
        }
        table.pack(**pack_kwargs, **extra_pack_options)

        return table


class ScrollableTreeViewDirector:
    def __init__(self, builder: ScrollableTreeViewBuilder):
        self._builder = builder

    def build_standard_tree_view(
        self, bindings: list[tuple[str, Callable, bool]] = []
    ) -> ScrollableTreeView:
        """Build a standard tree view with headings, browse selection, and default packing."""
        self._builder.with_show('headings').with_selectmode('browse')

        for binding in bindings:
            sequence, func, add = binding[0], binding[1], binding[2]
            self._builder.add_binding(sequence, func, add)

        self._builder.with_pack_side('left').with_pack_fill('both').with_pack_expand(True)

        return self._builder.build()

    def build_selectable_tree_view(
        self, bindings: list[tuple[str, Callable, bool]] = []
    ) -> ScrollableTreeView:
        """Build a tree view optimized for multiple selection."""
        self._builder.with_show('headings').with_selectmode('extended')

        for binding in bindings:
            sequence, func, add = binding[0], binding[1], binding[2]
            self._builder.add_binding(sequence, func, add)

        self._builder.with_pack_side('left').with_pack_fill('both').with_pack_expand(True)

        return self._builder.build()

    def build_compact_tree_view(
        self, height: int = 10, bindings: list[tuple[str, Callable, bool]] = []
    ) -> ScrollableTreeView:
        """Build a compact tree view with fixed height."""
        self._builder.with_show('headings').with_selectmode('browse').with_height(height)

        for binding in bindings:
            sequence, func, add = binding[0], binding[1], binding[2]
            self._builder.add_binding(sequence, func, add)

        self._builder.with_pack_side('left').with_pack_fill('both').with_pack_expand(
            False
        )

        return self._builder.build()

    def build_tree_only_view(
        self, bindings: list[tuple[str, Callable, bool]] = []
    ) -> ScrollableTreeView:
        """Build a tree view showing only the tree structure without headings."""
        self._builder.with_show('tree').with_selectmode('browse')

        for binding in bindings:
            sequence, func, add = binding[0], binding[1], binding[2]
            self._builder.add_binding(sequence, func, add)

        self._builder.with_pack_side('left').with_pack_fill('both').with_pack_expand(True)

        return self._builder.build()
