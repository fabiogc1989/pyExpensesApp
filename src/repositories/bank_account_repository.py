from src.core.database import SessionLocal, BankAccount
from src.models.database_schema import BankAccountSchema
from src.core.di import ioc
from .base_repository import BaseRepository


@ioc.register
class BankAccountRepository(BaseRepository[BankAccountSchema]):
    def get_all(self) -> list[BankAccountSchema]|iter[BankAccountSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(BankAccount).all()
                return [BankAccountSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            print(f'Erro na busca de contas: {e}')
            return []

    def get(self, id: int) -> BankAccountSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
            return BankAccountSchema.model_validate(entity) if entity else None
        except:
            return None

    def delete(self, id: int) -> bool:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
                if entity is not None:
                    session.delete(entity)
                    session.commit()
                else:
                    return False
            return True
        except:
            return False

    def update(self, entity: BankAccountSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_bank_account = BankAccount(**entity.model_dump())
                session.merge(db_bank_account)
                session.commit()
            return True
        except:
            return False
    
    def insert(self, entity: BankAccountSchema) -> bool:
        try:
            with SessionLocal() as session:
                db_bank_account = BankAccount(**entity.model_dump())
                session.add(db_bank_account)
                session.commit()
            return True
        except:
            return False