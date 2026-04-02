import tkinter as tk
from tkinter import ttk


def change_screen(container: tk.Tk|ttk.Frame, screen: ttk.Frame):
    if container._current_screen is not None:
        container._current_screen.destroy()
    container._current_screen = screen
    container._current_screen.tkraise() # Bring the selected screen to the front