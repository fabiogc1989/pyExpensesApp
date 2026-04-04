from tkinter import Menu

class MenuBuilder:
    def __init__(self, root):
        self.root = root
        self.menu_bar = Menu(master=self.root)
        self.stack = []
    
    @property
    def current_menu(self):
        return self.stack[-1] if self.stack else None

    def add_main_menu(self, label):
        main_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=label, menu=main_menu)
        self.stack = [main_menu]
        return self
    
    def add_sub_menu(self, label):
        if not self.stack:
            raise ValueError("No main menu defined. Call add_main_menu() first.")
        sub_menu = Menu(self.current_menu, tearoff=0)
        self.current_menu.add_cascade(label=label, menu=sub_menu)
        self.stack.append(sub_menu)
        return self

    def add_item(self, label, command = None):
        if self.current_menu is None:
            raise ValueError("No main menu defined. Call add_main_menu() first.")
        self.current_menu.add_command(label=label, command=command)
        return self
    
    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()
        return self
    
    def build(self):
        self.root.config(menu=self.menu_bar)
        return self.menu_bar