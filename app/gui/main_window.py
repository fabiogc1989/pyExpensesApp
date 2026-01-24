import tkinter as tk
from tkinter import ttk, Menu
from .screens import StartScreen, BankAccountScreen


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('pyExpenses')
        self.geometry('800x600')

        self._setup_widgets()

        # Container for screens
        self.container = tk.Frame(self)
        self.container.pack(fill='both', expand=True)

        # Initialize screens
        self.screens = {}
        for ScreenClass in (StartScreen, BankAccountScreen):
            frame = ScreenClass(self.container)
            self.screens[ScreenClass] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_screen(StartScreen)
        
    def _setup_widgets(self):
        # Create menu bar
        menu_bar = Menu(master=self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)

        # Bank Account Menu
        bank_account_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Bank Account", menu=bank_account_menu)
        bank_account_menu.add_command(label="View Accounts", command=lambda: self.show_screen(BankAccountScreen))

        # Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: print("Tkinter App v1.0"))
    
    def show_screen(self, screen_class):
        frame = self.screens[screen_class]
        frame.tkraise() # Bring the selected screen to the front