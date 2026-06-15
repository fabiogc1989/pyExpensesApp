from tkinter import messagebox, ttk
from typing import Optional, cast

from pydantic import ValidationError

from src.core.di import Inject
from src.exception.repository_exception import RepositoryException
from src.model.db_schema.bank_account_schema import BankAccountSchema
from src.repository.bank_account_repository import BankAccountRepository

from .form_modal import FormModal


class BankAccountFormModal(FormModal[BankAccountSchema]):
    __repo: BankAccountRepository = cast(
        BankAccountRepository, Inject(BankAccountRepository)
    )

    def __init__(self, master=None, model: Optional[BankAccountSchema] = None):
        super().__init__(master=master)

        self.success = False
        self.model = model

        # Modal's properties
        is_create = self.model is None
        self.edit_mode = 'create' if is_create else 'edit'
        self.title('Create Bank Account' if is_create else 'Edit Bank Account')

        # Design the modal
        self._setup_ui()

        self.focus_set()  # Focus on this window
        self.wait_window()  # Wait until it's closed

    def _setup_ui(self):
        """Organize the interface construction to keep __init__ clean."""
        self.__main_frame = ttk.Frame(master=self, padding=10)
        self.__main_frame.grid(row=0, column=0, sticky='nsew')

        # Iban Label and Entry
        self.ibanLabel = ttk.Label(master=self.__main_frame, text='IBAN:')
        self.ibanLabel.grid(row=0, column=0, sticky='w', pady=5)
        self.ibanEntry = ttk.Entry(master=self.__main_frame, width=40)
        self.ibanEntry.grid(row=0, column=1, sticky='ew', columnspan=2, pady=5)
        if self.model is not None and self.model.iban is not None:
            self.ibanEntry.insert(0, self.model.iban)

        # Buttons
        self.submitButton = ttk.Button(
            master=self.__main_frame, text='Save', command=self.on_submit
        )
        self.submitButton.grid(row=1, column=1, sticky='ew', pady=10, padx=2)
        self.cancelButton = ttk.Button(
            master=self.__main_frame, text='Cancel', command=self.destroy
        )
        self.cancelButton.grid(row=1, column=2, sticky='ew', pady=10, padx=2)

    def on_submit(self):
        try:
            iban_value = (
                self.ibanEntry.get().strip()
            )  # Collect IBAN from entry and remove extra spaces

            # Update or create the model using Pydantic for validation
            if self.edit_mode == 'create':
                # Create a new schema.
                # Note: debits and credits start as empty lists by default in your Schema
                self.model = BankAccountSchema(iban=iban_value)
                self.__repo.insert(self.model)
            else:
                # In edit mode, validate only the changed field
                # Pydantic will validate via @field_validator('iban')
                if self.model is None:
                    raise ValueError('Bank account object is None')
                self.model.iban = iban_value
                self.__repo.update(self.model)

            self.success = True
            self.destroy()
        except RepositoryException as e:
            # Capture repository-specific errors (e.g. duplicate IBAN)
            messagebox.showerror(
                'Repository Error', f'An error occurred while saving:\n{str(e)}'
            )
        except ValidationError as e:
            # Capture Pydantic errors (e.g. empty IBAN or negative ID)
            errors = '\n'.join(f'- {err["msg"]}' for err in e.errors())
            messagebox.showerror(
                'Validation Error', f'Please fix the following:\n{errors}'
            )
        except Exception as e:
            # Capture database errors or other unexpected issues
            messagebox.showerror('Exception', f'An unexpected error occurred:\n{str(e)}')
