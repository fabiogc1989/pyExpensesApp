from tkinter import ttk


class StartScreen(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        label = ttk.Label(self, text="Welcome to pyExpenses!", font=("Arial", 18))
        label.pack(pady=20)   