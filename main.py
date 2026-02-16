from app.gui.main_window import MainWindow
from core.database import init_db


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
