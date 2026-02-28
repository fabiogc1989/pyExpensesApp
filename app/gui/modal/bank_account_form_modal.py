from tkinter import ttk
from models.database_schema import BankAccountSchema
from repositories.bank_account_repository import BankAccountRepository

from .form_modal import FormModal


class BankAccountFormModal(FormModal[BankAccountSchema]):
    def __init__(self, master = None, model: BankAccountSchema = None):
        super().__init__(master=master)

        self.__repository = BankAccountRepository()

        # Modal's properties
        self.edit_mode = 'create' if model is None or model.id is None or model.id == 0 else 'edit'
        self.title('Create Bank Account') if self.edit_mode == 'create' else self.title('Edit Bank Account')
        self.model = model
        
        # Design the modal
        self.__main_frame = ttk.Frame(master=self, padding=10)
        self.__main_frame.grid(row=0, column=0, sticky='nsew')

        # Iban Label and Entry
        self.ibanLabel = ttk.Label(master=self.__main_frame, text="IBAN:")
        self.ibanLabel.grid(row=0, column=0, sticky='w', pady=5)
        self.ibanEntry = ttk.Entry(master=self.__main_frame, width=40)
        self.ibanEntry.grid(row=0, column=1, sticky='ew', columnspan=2,pady=5)
        if self.model is not None and self.model.iban is not None:
            self.ibanEntry.insert(0, self.model.iban)

        # Buttons
        self.submitButton = ttk.Button(master=self.__main_frame, text="Save", command=self.on_submit)
        self.submitButton.grid(row=1, column=1, sticky='ew', pady=10, padx=2)
        self.cancelButton = ttk.Button(master=self.__main_frame, text="Cancel", command=self.destroy)
        self.cancelButton.grid(row=1, column=2, sticky='ew', pady=10, padx=2)

        self.focus_set() # Focus on this window
        self.wait_window()  # Wait until it's closed

    def on_submit(self):
        if self.edit_mode == 'create':
            self.model = BankAccountSchema(iban=self.ibanEntry.get())
            self.__repository.insert(self.model)
        else:
            self.model.iban = self.ibanEntry.get()
            self.__repository.update(self.model)
        self.destroy()
