from src.core.database import SessionLocal, Credit
from src.models.database_schema import CreditSchema
from src.repositories.base_repository import BaseRepository
from src.core.di import ioc

@ioc.register
class CreditRepository(BaseRepository[CreditSchema]):
    def get_all(self) -> list[CreditSchema]|iter[CreditSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(Credit).all()
            return [CreditSchema.model_validate(entity) for entity in entities]
        except:
            return []

    def get(self, id: int) -> CreditSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(Credit, id)
            return CreditSchema.model_validate(entity) if entity else None
        except:
            return None

    def delete(self, id: int) -> bool:
        try:
            with SessionLocal() as session:
                entity = session.get(Credit, id)
                if entity is not None:
                    session.delete(entity)
                    session.commit()
                else:
                    return False
            return True
        except:
            return False

    def update(self, entity: CreditSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_credit = Credit(**entity.model_dump())
                session.merge(db_credit)
                session.commit()
            return True
        except:
            return False
    
    def insert(self, entity: CreditSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_credit = Credit(**entity.model_dump())
                session.add(db_credit)
                session.commit()
            return True
        except:
            return False