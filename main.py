from app.gui.main_window import MainWindow
from core.database import init_db
from tkinter import ttk, Toplevel

def create_bank_account_window(master, engine):
    backAccountWindow = Toplevel(master)
    backAccountWindow.title("Create Bank Account")
    backAccountWindow.resizable(False, False)
    backAccountWindow.transient(master) # Keep on top of the main window
    backAccountWindow.grab_set() # Make it modal
    backAccountWindow.focus_set() # Focus on this window

    backAccountFrame = ttk.Frame(master=backAccountWindow, padding=10)
    backAccountFrame.columnconfigure(0, weight=1)
    backAccountFrame.rowconfigure(0, weight=1)
    backAccountFrame.pack(fill='both', expand=True)
    backAccountFrame.grid(row=0, column=0, sticky="nsew")

    # Grid Layout

    # Row 0 - Iban Label and Entry
    ibanLabel = ttk.Label(master=backAccountFrame, text="IBAN:")
    ibanLabel.grid(row=0, column=0, sticky='w')
    ibanEntry = ttk.Entry(master=backAccountFrame, width=40)
    ibanEntry.grid(row=0, column=1, sticky='ew', columnspan=2)

    # Row 1 - submit & cancel buttons
    def on_submit():
        pass

    submitButton = ttk.Button(master=backAccountFrame, text="Save", command=on_submit)
    submitButton.grid(row=1, column=1, sticky='ew', pady=10)
    cancelButton = ttk.Button(master=backAccountFrame, text="Cancel", command=backAccountWindow.destroy)
    cancelButton.grid(row=1, column=2, sticky='ew', pady=10)

    backAccountWindow.wait_window()  # Wait until it's closed


def main():
    # Initialize the database
    init_db()

    # Initialize the main window
    main_window = MainWindow()

    # create_bank_account_window(main_window, engine)

    # Start the application
    main_window.mainloop()


if __name__ == "__main__":
    main()
