from collections.abc import Iterator
from typing import override

from src.core.database import Debit, SessionLocal
from src.core.di import ioc
from src.exception.repository_exception import RepositoryException
from src.model.db_schema.debit_schema import DebitSchema
from src.repository.base_repository import BaseRepository


@ioc.register
class DebitRepository(BaseRepository[DebitSchema]):
    @override
    def get_all(self) -> list[DebitSchema] | Iterator[DebitSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(Debit).all()
                return [DebitSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(f'Error fetching all debits: {str(e)}')

    @override
    def get(self, id: int) -> DebitSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(Debit, id)
                if entity is None:
                    raise RepositoryException(f'Debit with ID {id} not found')
                return DebitSchema.model_validate(entity)
        except Exception as e:
            raise RepositoryException(f'Error fetching debit with ID {id}: {str(e)}')

    @override
    def delete(self, id: int) -> None:
        try:
            with SessionLocal() as session:
                entity = session.get(Debit, id)
                if entity is None:
                    raise RepositoryException(f'Debit with ID {id} not found')
                session.delete(entity)
                session.commit()
        except Exception as e:
            raise RepositoryException(f'Error deleting debit with ID {id}: {str(e)}')

    @override
    def update(self, entity: DebitSchema) -> None:
        try:
            with SessionLocal() as session:
                db_debit = Debit(**entity.model_dump())
                session.merge(db_debit)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error updating debit with ID {entity.id}: {str(e)}'
            )

    @override
    def insert(self, entity: DebitSchema) -> None:
        try:
            with SessionLocal() as session:
                db_debit = Debit(**entity.model_dump())
                session.add(db_debit)
                session.commit()
        except Exception as e:
            raise RepositoryException(
                f'Error inserting debit with ID {entity.id}: {str(e)}'
            )
