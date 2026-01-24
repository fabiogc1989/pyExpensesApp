import tkinter as tk
from tkinter import ttk


class StartScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = ttk.Label(self, text="Welcome to pyExpenses!", font=("Arial", 18))
        label.pack(pady=20)


class BankAccountScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = ttk.Label(self, text="Bank Accounts", font=("Arial", 18))
        label.pack(pady=20)