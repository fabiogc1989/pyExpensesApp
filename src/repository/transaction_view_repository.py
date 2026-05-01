from typing import override

from src.core.database import SessionLocal, TransactionView
from src.exception.repository_exception import RepositoryException
from src.model.db_schema.transaction_vew_schema import TransactionViewSchema
from src.model.transaction_search import TransactionSearch
from src.repository.base_repository import BaseReadRepository
from src.core.di import ioc

@ioc.register
class TransactionViewRepository(BaseReadRepository[TransactionViewSchema]):
    @override
    def get_all(self) -> list[TransactionViewSchema]|iter[TransactionViewSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(TransactionView).all()
            return [TransactionViewSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(f"Error fetching all transaction views: {str(e)}")
    
    @override
    def get(self, id: int) -> TransactionViewSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(TransactionView, id)
            if entity is None:
                raise RepositoryException(f"Transaction view with ID {id} not found")
            return TransactionViewSchema.model_validate(entity)
        except Exception as e:
            raise RepositoryException(f"Error fetching transaction view with ID {id}: {str(e)}")
    
    
    def search_transactions(self, search_model: TransactionSearch) -> list[TransactionViewSchema]|iter[TransactionViewSchema]:
        try:
            with SessionLocal() as session:
                query = session.query(TransactionView)

                if search_model.iban is not None:
                    query = query.filter(TransactionView.bank_account.has(iban = search_model.iban))
                if search_model.min_amount is not None:
                    query = query.filter(TransactionView.amount >= search_model.min_amount)
                if search_model.max_amount is not None:
                    query = query.filter(TransactionView.amount <= search_model.max_amount)
                if search_model.start_date is not None:
                    query = query.filter(TransactionView.date >= search_model.start_date)
                if search_model.end_date is not None:
                    query = query.filter(TransactionView.date <= search_model.end_date)
                if search_model.type is not None and search_model.type != search_model.type.ALL:
                    query = query.filter(TransactionView.type == search_model.type.name)
                if search_model.description is not None:
                    query = query.filter(TransactionView.description.ilike(f"%{search_model.description}%"))

                entities = query.all()
            return [TransactionViewSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(f"Error searching transactions: {str(e)}")