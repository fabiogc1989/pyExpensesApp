from tkinter import Toplevel


class BaseModal(Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.resizable(False, False)
        self.transient(master=master) # Keep on top of the main window
        self.wait_visibility() # Wait until it's visible before grabbing focus
        self.grab_set() # Make it modal