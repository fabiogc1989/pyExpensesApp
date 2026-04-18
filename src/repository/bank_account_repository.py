from src.core.database import SessionLocal, BankAccount
from src.exception.repository_exception import RepositoryException
from src.model.db_schema.bank_account_schema import BankAccountSchema
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
            raise RepositoryException(f"Error retrieving all bank accounts: {str(e)}")

    def get(self, id: int) -> BankAccountSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
            if entity is None:
                raise RepositoryException(f"Bank account with ID {id} not found")
            return BankAccountSchema.model_validate(entity)
        except Exception as e:
            raise RepositoryException(f"Error retrieving bank account with ID {id}: {str(e)}")

    def delete(self, id: int) -> None:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
                if entity is None:
                    raise RepositoryException(f"Bank account with ID {id} not found")
                session.delete(entity)
                session.commit()
        except Exception as e:
            raise RepositoryException(f"Error deleting bank account with ID {id}: {str(e)}")

    def update(self, entity: BankAccountSchema) -> None:
        try:
            with SessionLocal() as session:
                db_bank_account = BankAccount(**entity.model_dump())
                session.merge(db_bank_account)
                session.commit()
        except Exception as e:
            raise RepositoryException(f"Error updating bank account with ID {entity.id}: {str(e)}")
    
    def insert(self, entity: BankAccountSchema) -> None:
        try:
            with SessionLocal() as session:
                db_bank_account = BankAccount(**entity.model_dump())
                session.add(db_bank_account)
                session.commit()
        except Exception as e:
            raise RepositoryException(f"Error inserting bank account with ID {entity.id}: {str(e)}")