from src.core.database import init_db
from src.gui.main_window import MainWindow


def main():
    # Initialize the database
    init_db()

    # Initialize the main window
    main_window = MainWindow()

    # Start the application
    main_window.mainloop()


if __name__ == '__main__':
    main()
