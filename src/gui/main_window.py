import tkinter as tk

from src.model.design_pattern.creational_pattern.menu_builder import MenuBuilder, MenuDirector
from src.util.gui import change_screen
from .screen.start_screen import StartScreen


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('pyExpenses')
        self._setup_widgets()
    
    @property
    def container(self):
        return self.__container
    
    @container.setter
    def container(self, container):
        self.__container = container

    @property
    def current_screen(self):
        return self.__current_screen
    
    @current_screen.setter
    def current_screen(self, screen):
        self.__current_screen = screen
        
    def _setup_widgets(self):     
        # Container for screens
        self.__container = tk.Frame(self)
        self.__container.pack(fill="both", expand=True)

        menu_builder = MenuBuilder(self)
        MenuDirector(menu_builder).build_app_menu(self)

        # Initialize screens
        self.current_screen = None
        change_screen(self, StartScreen(self.__container))
