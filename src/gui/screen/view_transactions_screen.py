import tkinter as tk 
from tkinter import ttk
from tkcalendar import DateEntry

from src.core.di import Inject
from src.model.design_pattern.creational_pattern.scrollable_tree_view_builder import ScrollableTreeViewBuilder, ScrollableTreeViewDirector
from src.model.transaction_search import TransactionSearch
from src.model.transaction_type import TransactionType
from src.repository.transaction_view_repository import TransactionViewRepository
from src.service.transaction_service import TransactionService


class ViewTransactionsScreen(ttk.Frame):
    __service: TransactionService = Inject(TransactionService)

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        search_frame = ttk.Frame(self)

        for i in range(12):
            search_frame.columnconfigure(i, weight=1)
            search_frame.rowconfigure(i, weight=0)
        
        search_model = self.__service.get_search_model()

        bank_account_label = ttk.Label(search_frame, text="IBAN")
        bank_account_label.grid(row=0, column=0, sticky=tk.EW, columnspan=6)
        self.bank_account_combobox = ttk.Combobox(search_frame, state="readonly", values=search_model.ibanList)
        self.bank_account_combobox.grid(row=1, column=0, sticky=tk.EW, columnspan=6, pady=10, padx=(0, 10))
        
        min_amount_label = ttk.Label(search_frame, text="Min. Amount")
        min_amount_label.grid(row=2, column=0, sticky=tk.EW, columnspan=3)
        self.min_amount_entry = ttk.Entry(search_frame, validate="key", validatecommand=(self.register(self._validate_amount_entry), '%P'))
        self.min_amount_entry.grid(row=3, column=0, sticky=tk.EW, columnspan=3, pady=10, padx=(0, 10))

        max_amount_label = ttk.Label(search_frame, text="Max. Amount")
        max_amount_label.grid(row=2, column=3, sticky=tk.EW, columnspan=3)
        self.max_amount_entry = ttk.Entry(search_frame, validate="key", validatecommand=(self.register(self._validate_amount_entry), '%P'))
        self.max_amount_entry.grid(row=3, column=3, sticky=tk.EW, columnspan=3, pady=10, padx=(0, 10))

        min_date_label = ttk.Label(search_frame, text="Min. Date")
        min_date_label.grid(row=0, column=6, sticky=tk.EW, columnspan=3)
        self.min_date_entry = DateEntry(
            search_frame,
            date_pattern='y-mm-dd' # Formato ISO para facilitar salvar no banco
        )
        self.min_date_entry.grid(row=1, column=6, sticky=tk.EW, columnspan=3, pady=10, padx=(0, 10))

        max_date_label = ttk.Label(search_frame, text="Max. Date")
        max_date_label.grid(row=0, column=9, sticky=tk.EW, columnspan=3)
        self.max_date_entry = DateEntry(
            search_frame,
            date_pattern='y-mm-dd' # Formato ISO para facilitar salvar no banco
        )
        self.max_date_entry.grid(row=1, column=9, sticky=tk.EW, columnspan=3, pady=10)

        transaction_type_label = ttk.Label(search_frame, text="Transaction Type")
        transaction_type_label.grid(row=2, column=6, sticky=tk.EW, columnspan=3)
        self.transaction_type_combobox = ttk.Combobox(search_frame, state="readonly", values=[t.name for t in TransactionType])
        self.transaction_type_combobox.grid(row=3, column=6, sticky=tk.EW, columnspan=6, pady=10)
        self.transaction_type_combobox.set(TransactionType.ALL.name)

        search_button = ttk.Button(search_frame, text="Search", command=self._search_transactions)
        search_button.grid(row=4, column=11, sticky=tk.EW)
        search_frame.pack(fill="x", padx=10, pady=10)

        scrollableTreeViewDirrector = ScrollableTreeViewDirector(ScrollableTreeViewBuilder(master=self, columns=('Transaction ID', 'Description', 'Amount', 'Date', 'Type', 'IBAN')))
        self.table = scrollableTreeViewDirrector.build_standard_tree_view()
        self._search_transactions()
        
    def _validate_amount_entry(self, P):
        if P == "" or P.replace(".", "", 1).isdigit():
            return True
        return False
    
    def _search_transactions(self):
        search_model = TransactionSearch(
            iban=self.bank_account_combobox.get() if self.bank_account_combobox.get() else None,
            min_amount=float(self.min_amount_entry.get()) if self.min_amount_entry.get() else None,
            max_amount=float(self.max_amount_entry.get()) if self.max_amount_entry.get() else None,
            min_date=self.min_date_entry.get_date(),
            max_date=self.max_date_entry.get_date(),
            type=TransactionType[self.transaction_type_combobox.get()]
        )
        results = self.__service.search_transactions(search_model)
        # Clear existing data
        for item in self.table.tree_view.get_children():
            self.table.tree_view.delete(item)
        # Insert new data
        for item in results:
            self.table.tree_view.insert(parent="", index=tk.END, iid=item.row_number, values=(item.transaction_id, item.description, item.amount, item.date, item.type.name, item.iban))