from models.bank_account import BankAccount
from .base_repository import BaseRepository

class BankAccountRepository(BaseRepository[BankAccount]):
    def get_all(self) -> list[BankAccount]|iter[BankAccount]:
        ...

    def get(self, id: int) -> BankAccount:
        ...

    def delete(self, entity: BankAccount) -> bool:
        ...

    def update(self, entity: BankAccount) -> bool:
        ...
    
    def insert(self, entity: BankAccount) -> bool:
        ...