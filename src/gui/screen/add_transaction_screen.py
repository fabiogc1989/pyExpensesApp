import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkcalendar import DateEntry

from src.core.di import ioc
from src.models.transaction_type import TransactionType
from src.repositories.bank_account_repository import BankAccountRepository
from src.repositories.credit_repository import CreditRepository
from src.repositories.debit_repository import DebitRepository


class AddTransactionScreen(ttk.Frame):
    @ioc.inject
    def __init__(self, master, transaction_type: TransactionType, bank_account_repo: BankAccountRepository, debit_repo: DebitRepository, credit_repo: CreditRepository):
        super().__init__(master)

        self.transaction_type = transaction_type
        print(f"Initializing AddTransactionScreen for {self.transaction_type.name}")
        self.bank_account_repo = bank_account_repo
        self.debit_repo = debit_repo
        self.credit_repo = credit_repo

        self.pack(fill="both", expand=True, padx=10, pady=10)
        # 1. Configurar as proporções das linhas e colunas (Grid 12x12)
        for i in range(12):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=0)
        
        self._setup_widgets()
        
        
    def _setup_widgets(self):
        # Configurar os widgets para seleção de conta bancária
        bank_account_label = ttk.Label(self, text="Select a bank account")
        bank_account_label.grid(row=0, column=0, sticky=tk.EW, columnspan=12)
        self.bank_account_combobox = ttk.Combobox(self, state="readonly")
        self.bank_account_combobox.grid(row=1, column=0, sticky=tk.EW, columnspan=12, pady=10)

        # Configurar os widgets para amount e date
        amount_label = ttk.Label(self, text="Amount")
        amount_label.grid(row=2, column=0, sticky=tk.EW, columnspan=5)
        self.amount_entry = ttk.Entry(self, validate="key", validatecommand=(self.register(self._validate_amount_entry), '%P'))
        self.amount_entry.grid(row=3, column=0, sticky=tk.EW, columnspan=5, pady=10)
        date_label = ttk.Label(self, text="Date")
        date_label.grid(row=2, column=7, sticky=tk.EW, columnspan=5)
        self.date_entry = DateEntry(
            self,
            date_pattern='y-mm-dd' # Formato ISO para facilitar salvar no banco
        )
        self.date_entry.grid(row=3, column=7, sticky=tk.EW, columnspan=5, pady=10)

        # Configurar os widgets para descrição
        description_label = ttk.Label(self, text="Description")
        description_label.grid(row=4, column=0, sticky=tk.EW, columnspan=12)
        self.description_entry = ScrolledText(self, height=10, undo=True, wrap=tk.WORD) 
        self.description_entry.grid(row=5, column=0, sticky=tk.EW, columnspan=12, pady=10)

        # Configurar o botão de salvar
        save_button = ttk.Button(self, text="Save")
        save_button.grid(row=6, column=11, sticky=tk.EW)

    def _validate_amount_entry(self, P):
        if P == "" or P.replace(".", "", 1).isdigit():
            return True
        return False