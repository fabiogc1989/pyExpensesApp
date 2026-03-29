from src.core.database import SessionLocal, Debit
from src.models.database_schema import DebitSchema
from src.repositories.base_repository import BaseRepository
from src.core.di import ioc

@ioc.register
class DebitRepository(BaseRepository[DebitSchema]):
    def get_all(self) -> list[DebitSchema]|iter[DebitSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(Debit).all()
            return [DebitSchema.model_validate(entity) for entity in entities]
        except:
            return []

    def get(self, id: int) -> DebitSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(Debit, id)
            return DebitSchema.model_validate(entity) if entity else None
        except:
            return None

    def delete(self, entity: DebitSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_debit = Debit(**entity.model_dump())
                session.delete(db_debit)
                session.commit()
            return True
        except:
            return False

    def update(self, entity: DebitSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_debit = Debit(**entity.model_dump())
                session.merge(db_debit)
                session.commit()
            return True
        except:
            return False
    
    def insert(self, entity: DebitSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_debit = Debit(**entity.model_dump())
                session.add(db_debit)
                session.commit()
            return True
        except Exception as e:
            print(f"Error occurred while inserting debit: {e}")
            return False