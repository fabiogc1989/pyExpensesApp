import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from pydantic import ValidationError
from tkcalendar import DateEntry

from src.core.di import ioc
from src.exception.repository_exception import RepositoryException
from src.model.database_schema import CreditSchema, DebitSchema
from src.model.transaction_type import TransactionType
from src.repository.bank_account_repository import BankAccountRepository
from src.repository.credit_repository import CreditRepository
from src.repository.debit_repository import DebitRepository


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
        self._load_bank_accounts()

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
        save_button = ttk.Button(self, text="Save", command=self.on_submit)
        save_button.grid(row=6, column=11, sticky=tk.EW)
    
    def _load_bank_accounts(self):
        try:
            self._bank_accounts = self.bank_account_repo.get_all()
            
            # Preencher o Combobox apenas com os IBANs
            self.bank_account_combobox['values'] = [account.iban for account in self._bank_accounts]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bank accounts:\n{str(e)}")

    def _validate_amount_entry(self, P):
        if P == "" or P.replace(".", "", 1).isdigit():
            return True
        return False
    
    def on_submit(self):
        try:
            # Criar a transação usando os repositórios
            selected_iban = self.bank_account_combobox.get()
            bank_account = next((acct for acct in self._bank_accounts if acct.iban == selected_iban), None)
            amount = float(self.amount_entry.get())
            date = self.date_entry.get_date()
            description = self.description_entry.get(1.0, tk.END).strip()

            if self.transaction_type == TransactionType.DEBIT:
                entity = DebitSchema(description=description, amount=amount, date=date, bank_account_id=bank_account.id)
                self.debit_repo.insert(entity)
            else:
                entity = CreditSchema(description=description, amount=amount, date=date, bank_account=bank_account)
                self.credit_repo.insert(entity)

            messagebox.showinfo("Success", f"{self.transaction_type.name.capitalize()} transaction added successfully!")
        except RepositoryException as e:
            # Capture repository-specific errors (e.g. database connection issues)
            messagebox.showerror("Repository Error", f"Failed to save transaction:\n{str(e)}")
        except ValidationError as e:
            # Capture Pydantic errors (e.g. empty IBAN or negative ID)
            errors = '\n'.join(f'- {err["msg"]}' for err in e.errors())
            messagebox.showerror('Validation Error', f'Please fix the following:\n{errors}')
        except Exception as e:
            # Capture database errors or other unexpected issues
            messagebox.showerror("Exception", f"An unexpected error occurred:\n{str(e)}")