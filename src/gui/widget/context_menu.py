from typing import Callable, List, Tuple
import tkinter as tk


class ContextMenu(tk.Menu):
    def __init__(self, commands: List[Tuple[str, Callable, bool]], master = None,):
        super().__init__(master, tearoff=0)

        for label, command, separator in commands:
            self.add_command(label=label, command=command)
            if separator:
                self.add_separator()
        
    def show_menu(self, event):
        try:
            self.tk_popup(event.x_root, event.y_root)
        finally:
            self.grab_release()