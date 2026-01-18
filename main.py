from models import Base, BankAccount
from tkinter import Tk, ttk, Toplevel, Menu
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

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
        with Session(engine) as session:
            bank_account = BankAccount(iban=ibanEntry.get())
            session.add(bank_account)
            session.commit()
        backAccountWindow.destroy()

    submitButton = ttk.Button(master=backAccountFrame, text="Save", command=on_submit)
    submitButton.grid(row=1, column=1, sticky='ew', pady=10)
    cancelButton = ttk.Button(master=backAccountFrame, text="Cancel", command=backAccountWindow.destroy)
    cancelButton.grid(row=1, column=2, sticky='ew', pady=10)

    backAccountWindow.wait_window()  # Wait until it's closed


def main():
    engine = create_engine('sqlite+pysqlite:///expenses.db', echo=True)
    Base.metadata.create_all(engine)
    
    # Initialize the root window
    root = Tk()
    root.title('pyExpenses')

    # Create menu bar
    menu_bar = Menu(master=root)
    root.config(menu=menu_bar)

    # File menu
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='File', menu=file_menu)

    # Help menu
    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)

    help_menu.add_command(label="About", command=lambda: print("Tkinter App v1.0"))

    # Create the frame and "pack" it into the window
    # We add padding so the content doesn't touch the edges
    mainFrame = ttk.Frame(master=root, padding=10)
    mainFrame.pack(fill='both', expand=True)

    create_bank_account_window(root, engine)

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
