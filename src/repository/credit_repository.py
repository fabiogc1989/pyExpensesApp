from collections.abc import Iterator
from typing import override

from src.core.database import Credit, SessionLocal
from src.core.di import ioc
from src.exception.repository_exception import RepositoryException
from src.model.db_schema.credit_schema import CreditSchema
from src.repository.base_repository import BaseRepository


@ioc.register
class CreditRepository(BaseRepository[CreditSchema]):
    @override
    def get_all(self) -> list[CreditSchema] | Iterator[CreditSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(Credit).all()
                return [CreditSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(f'Error fetching all credits: {str(e)}')

    @override
    def get(self, id: int) -> CreditSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(Credit, id)
                if entity is None:
                    raise RepositoryException(f'Credit with ID {id} not found')
                return CreditSchema.model_validate(entity)
        except Exception as e:
            raise RepositoryException(f'Error fetching credit with ID {id}: {str(e)}')

    @override
    def delete(self, id: int) -> None:
        try:
            with SessionLocal() as session:
                entity = session.get(Credit, id)
                if entity is None:
                    raise RepositoryException(f'Credit with ID {id} not found')
                session.delete(entity)
                session.commit()
        except Exception as e:
            raise RepositoryException(f'Error deleting credit with ID {id}: {str(e)}')

    @override
    def update(self, entity: CreditSchema) -> None:
        try:
            with SessionLocal() as session:
                db_credit = Credit(**entity.model_dump())
                session.merge(db_credit)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error updating credit with ID {entity.id}: {str(e)}'
            )

    @override
    def insert(self, entity: CreditSchema) -> None:
        try:
            with SessionLocal() as session:
                db_credit = Credit(**entity.model_dump())
                session.add(db_credit)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error inserting credit with ID {entity.id}: {str(e)}'
            )
