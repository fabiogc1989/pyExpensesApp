from core.database import SessionLocal, Credit
from repositories.base_repository import BaseRepository


class CreditRepository(BaseRepository[Credit]):
    def get_all(self) -> list[Credit]|iter[Credit]:
        try:
            with SessionLocal() as session:
                entities = session.query(Credit).all()
            return entities
        except:
            return []

    def get(self, id: int) -> Credit:
        try:
            with SessionLocal() as session:
                entity = session.get(Credit, id)
            return entity
        except:
            return None

    def delete(self, entity: Credit) -> bool:
        try:
            with SessionLocal() as session:
                session.delete(entity)
                session.commit()
            return True
        except:
            return False

    def update(self, entity: Credit) -> bool:
        try:
            with SessionLocal() as session:
                session.merge(entity)
                session.commit()
            return True
        except:
            return False
    
    def insert(self, entity: Credit) -> bool:
        try:
            with SessionLocal() as session:
                session.add(entity)
                session.commit()
            return True
        except:
            return False