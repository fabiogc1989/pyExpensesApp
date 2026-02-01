from core.database import SessionLocal, Debit
from repositories.base_repository import BaseRepository


class DebitRepository(BaseRepository[Debit]):
    def get_all(self) -> list[Debit]|iter[Debit]:
        try:
            with SessionLocal() as session:
                entities = session.query(Debit).all()
            return entities
        except:
            return []

    def get(self, id: int) -> Debit:
        try:
            with SessionLocal() as session:
                entity = session.get(Debit, id)
            return entity
        except:
            return None

    def delete(self, entity: Debit) -> bool:
        try:
            with SessionLocal() as session:
                session.delete(entity)
                session.commit()
            return True
        except:
            return False

    def update(self, entity: Debit) -> bool:
        try:
            with SessionLocal() as session:
                session.merge(entity)
                session.commit()
            return True
        except:
            return False
    
    def insert(self, entity: Debit) -> bool:
        try:
            with SessionLocal() as session:
                session.add(entity)
                session.commit()
            return True
        except:
            return False