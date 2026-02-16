from .base_modal import BaseModal
from tkinter import ttk


class BankAccountFormModal(BaseModal):
    def __init__(self, master = None):
        super().__init__(master=master)

        # Modal's properties
        self.title('Create Bank Account')
        
        # Design the modal
        self.__setup_widgets()
        self.focus_set() # Focus on this window

        self.wait_window()  # Wait until it's closed

    def __setup_widgets(self):
        main_frame = ttk.Frame(master=self, padding=10)
        #frame.columnconfigure(0, weight=1)
        #frame.rowconfigure(0, weight=1)
        #frame.pack(fill='both', expand=True)
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Iban Label and Entry
        ibanLabel = ttk.Label(master=main_frame, text="IBAN:")
        ibanLabel.grid(row=0, column=0, sticky='w', pady=5)
        ibanEntry = ttk.Entry(master=main_frame, width=40)
        ibanEntry.grid(row=0, column=1, sticky='ew', columnspan=2,pady=5)

        # Buttons
        submitButton = ttk.Button(master=main_frame, text="Save", command=self.on_submit)
        submitButton.grid(row=1, column=1, sticky='ew', pady=10, padx=2)
        cancelButton = ttk.Button(master=main_frame, text="Cancel", command=self.destroy)
        cancelButton.grid(row=1, column=2, sticky='ew', pady=10, padx=2)

    def on_submit(self):
        pass
