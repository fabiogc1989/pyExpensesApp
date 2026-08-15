from collections.abc import Iterator
from typing import override

from src.core.database import BankAccount, SessionLocal
from src.core.di import ioc
from src.exception.repository_exception import RepositoryException
from src.model.bank_account_search import BankAccountSearch
from src.model.db_schema.bank_account_schema import BankAccountSchema

from .base_repository import BaseRepository


@ioc.register
class BankAccountRepository(BaseRepository[BankAccountSchema]):
    @override
    def get_all(self) -> list[BankAccountSchema] | Iterator[BankAccountSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(BankAccount).all()
                return [BankAccountSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(f'Error retrieving all bank accounts: {str(e)}')

    @override
    def get(self, id: int) -> BankAccountSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
                if entity is None:
                    raise RepositoryException(f'Bank account with ID {id} not found')
                return BankAccountSchema.model_validate(entity)
        except Exception as e:
            raise RepositoryException(
                f'Error retrieving bank account with ID {id}: {str(e)}'
            )

    @override
    def delete(self, id: int) -> None:
        try:
            with SessionLocal() as session:
                entity = session.get(BankAccount, id)
                if entity is None:
                    raise RepositoryException(f'Bank account with ID {id} not found')
                session.delete(entity)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error deleting bank account with ID {id}: {str(e)}'
            )

    @override
    def update(self, entity: BankAccountSchema) -> None:
        try:
            with SessionLocal() as session:
                db_bank_account = BankAccount(**entity.model_dump())
                session.merge(db_bank_account)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error updating bank account with ID {entity.id}: {str(e)}'
            )

    @override
    def insert(self, entity: BankAccountSchema) -> None:
        try:
            with SessionLocal() as session:
                db_bank_account = BankAccount(**entity.model_dump())
                session.add(db_bank_account)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error inserting bank account with ID {entity.id}: {str(e)}'
            )

    def search_bank_accounts(self,search_model: BankAccountSearch) -> list[BankAccountSchema] | Iterator[BankAccountSchema]:
        try:
            with SessionLocal() as session:
                query = session.query(BankAccount)

                if search_model.iban is not None and search_model.iban != '':
                    query = query.filter(BankAccount.iban == search_model.iban)

                entities = query.all()
                return [BankAccountSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(
                f'Error searching bank accounts: {str(e)}'
            )
