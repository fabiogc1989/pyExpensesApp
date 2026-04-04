import tkinter as tk

from src.gui.screen.add_transaction_screen import AddTransactionScreen
from src.model.design_pattern.creational_pattern.menu_builder import MenuBuilder
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
        
    def _setup_widgets(self):
        menu_builder = MenuBuilder(self)

        # Add File menu
        menu_builder\
            .add_main_menu('File')
        
        # Add Bank Account menu
        menu_builder\
            .add_main_menu('Bank Account')\
                .add_item('Add Account', command=lambda: BankAccountFormModal())\
                .add_item('View Accounts', command=lambda: change_screen(self, BankAccountScreen(self.container)))
        
        # Add Transaction menu
        menu_builder\
            .add_main_menu('Transaction')\
                .add_sub_menu('Add')\
                    .add_item('Debit', command=lambda: change_screen(self, AddTransactionScreen(self.container, transaction_type=TransactionType.DEBIT)))\
                    .add_item('Credit', command=lambda: change_screen(self, AddTransactionScreen(self.container, transaction_type=TransactionType.CREDIT)))\
                .back()\
                .add_item('View Transactions', command=lambda: print("View Transactions clicked"))
        
        # Add Help menu
        menu_builder\
            .add_main_menu('Help')\
                .add_item('About', command=lambda: change_screen(self, StartScreen(self.container)))
        
        # Build the menu
        menu_builder.build()
        
        # Container for screens
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Initialize screens
        self._current_screen = None        
        change_screen(self, StartScreen(self.container))
