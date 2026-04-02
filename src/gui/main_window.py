import tkinter as tk

from src.gui.screen.add_transaction_screen import AddTransactionScreen
from src.model.transaction_type import TransactionType
from src.model.transaction_type import TransactionType
from src.util.gui import change_screen
from .modal.bank_account_form_modal import BankAccountFormModal
from .screen.start_screen import StartScreen
from .screen.bank_account_screen import BankAccountScreen


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('pyExpenses')
        # self.geometry('800x600')

        self._setup_widgets()

        # Container for screens
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Initialize screens
        self._current_screen = None        
        change_screen(self, StartScreen(self.container))
        
    def _setup_widgets(self):
        # Create menu bar
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)

        # Bank Account Menu
        bank_account_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Bank Account", menu=bank_account_menu)
        bank_account_menu.add_command(label='Add Account', command=lambda: BankAccountFormModal())
        bank_account_menu.add_command(label='View Accounts', command=lambda: change_screen(self, BankAccountScreen(self.container)))

        # Transaction Menu
        transaction_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='Transaction', menu=transaction_menu)
        
        transaction_add_menu = tk.Menu(transaction_menu, tearoff=0)
        transaction_add_menu.add_command(label='Debit', command=lambda: change_screen(self, AddTransactionScreen(self.container, transaction_type=TransactionType.DEBIT)))
        transaction_add_menu.add_command(label='Credit', command=lambda: change_screen(self, AddTransactionScreen(self.container, transaction_type=TransactionType.CREDIT)))

        transaction_menu.add_cascade(label='Add', menu=transaction_add_menu)
        transaction_menu.add_command(label='View Transactions', command=lambda: print("View Transactions clicked"))

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: change_screen(self, StartScreen))
