from typing import Literal

from .base_modal import BaseModal

class FormModal[T](BaseModal):
    def __init__(self, master = None):
        super().__init__(master=master)
    
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model: T):
        self._model = model

    @property
    def edit_mode(self):
        return self._edit_mode
    
    @edit_mode.setter
    def edit_mode(self, mode: Literal['create', 'edit']):
        self._edit_mode = mode
