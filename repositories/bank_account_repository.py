from core.database import SessionLocal
from models.bank_account import BankAccount
from .base_repository import BaseRepository

class BankAccountRepository(BaseRepository[BankAccount]):
    def get_all(self) -> list[BankAccount]|iter[BankAccount]:
        try:
            with SessionLocal() as session:
                entities = session.query(BankAccount).all()
            return entities
        except:
            return []

    def get(self, id: int) -> BankAccount:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
            return entity
        except:
            return None

    def delete(self, entity: BankAccount) -> bool:
        try:
            with SessionLocal() as session:
                session.delete(entity)
                session.commit()
            return True
        except:
            return False

    def update(self, entity: BankAccount) -> bool:
        try:
            with SessionLocal() as session:
                session.merge(entity)
                session.commit()
            return True
        except:
            return False
    
    def insert(self, entity: BankAccount) -> bool:
        try:
            with SessionLocal() as session:
                session.add(entity)
                session.commit()
            return True
        except:
            return False