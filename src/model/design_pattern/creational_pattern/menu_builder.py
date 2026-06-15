from tkinter import Menu

from src.gui.modal.bank_account_form_modal import BankAccountFormModal
from src.gui.screen.add_transaction_screen import AddTransactionScreen
from src.gui.screen.bank_account_screen import BankAccountScreen
from src.gui.screen.start_screen import StartScreen
from src.gui.screen.view_transactions_screen import ViewTransactionsScreen
from src.model.transaction_type import TransactionType
from src.util.gui import change_screen


class MenuBuilder:
    def __init__(self, root):
        self._root = root
        self._menu_bar = Menu(master=self._root)
        self._stack = []

    @property
    def current_menu(self):
        return self._stack[-1]

    def add_main_menu(self, label):
        main_menu = Menu(self._menu_bar, tearoff=0)
        self._menu_bar.add_cascade(label=label, menu=main_menu)
        self._stack = [main_menu]
        return self

    def add_sub_menu(self, label):
        if not self._stack:
            raise ValueError('No main menu defined. Call add_main_menu() first.')
        sub_menu = Menu(self.current_menu, tearoff=0)
        self.current_menu.add_cascade(label=label, menu=sub_menu)
        self._stack.append(sub_menu)
        return self

    def add_item(self, label, command):
        if self.current_menu is None:
            raise ValueError('No main menu defined. Call add_main_menu() first.')
        self.current_menu.add_command(label=label, command=command)
        return self

    def back(self):
        if len(self._stack) > 1:
            self._stack.pop()
        return self

    def build(self):
        self._root.config(menu=self._menu_bar)
        return self._menu_bar


class MenuDirector:
    def __init__(self, builder: MenuBuilder):
        self._builder = builder

    def build_app_menu(self, master):
        # Add File menu
        self._builder.add_main_menu('File')

        # Add Bank Account menu
        self._builder.add_main_menu('Bank Account').add_item(
            'Add Account', command=lambda: BankAccountFormModal()
        ).add_item(
            'View Accounts',
            command=lambda: change_screen(master, BankAccountScreen(master.container)),
        )

        # Add Transaction menu
        self._builder.add_main_menu('Transaction').add_sub_menu('Add').add_item(
            'Debit',
            command=lambda: change_screen(
                master,
                AddTransactionScreen(
                    master.container, transaction_type=TransactionType.DEBIT
                ),
            ),
        ).add_item(
            'Credit',
            command=lambda: change_screen(
                master,
                AddTransactionScreen(
                    master.container, transaction_type=TransactionType.CREDIT
                ),
            ),
        ).back().add_item(
            'View Transactions',
            command=lambda: change_screen(
                master, ViewTransactionsScreen(master.container)
            ),
        )

        # Add Help menu
        self._builder.add_main_menu('Help').add_item(
            'About', command=lambda: change_screen(master, StartScreen(master.container))
        )

        return self._builder.build()
