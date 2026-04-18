import tkinter as tk
from tkinter import ttk


def change_screen(container: tk.Tk|ttk.Frame, screen: ttk.Frame):
    if container.current_screen is not None:
        container.current_screen.destroy()
    container.current_screen = screen
    container.current_screen.tkraise() # Bring the selected screen to the front