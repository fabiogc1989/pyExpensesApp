from models import Base
from tkinter import Tk, ttk, Toplevel
from sqlalchemy import create_engine, text


def main():
    engine = create_engine('sqlite+pysqlite:///expenses.db', echo=True)
    Base.metadata.create_all(engine)
    with engine.connect() as connection:
        result = connection.execute(text("select 'hello world'"))
        print(result.all())
    
    # Initialize the root window
    root = Tk()
    root.title('pyExpenses')

    # Create the frame and "pack" it into the window
    # We add padding so the content doesn't touch the edges
    mainFrame = ttk.Frame(master=root, padding=10)
    mainFrame.pack(fill='both', expand=True)

    #Top level for bank accounts
    backAccountWindow = Toplevel(root)
    backAccountWindow.title("Create Bank Account")
    backAccountWindow.resizable(False, False)
    backAccountWindow.transient(root) # Keep on top of the main window
    backAccountWindow.grab_set()      # Make it modal
    backAccountWindow.focus_set()     # Focus on this window
    
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
    submitButton = ttk.Button(master=backAccountFrame, text="Save")
    submitButton.grid(row=1, column=1, sticky='ew', pady=10)
    cancelButton = ttk.Button(master=backAccountFrame, text="Cancel", command=backAccountWindow.destroy)
    cancelButton.grid(row=1, column=2, sticky='ew', pady=10)

    backAccountWindow.wait_window()  # Wait until it's closed


    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
