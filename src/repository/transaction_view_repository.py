from src.core.database import SessionLocal, TransactionView
from src.exception.repository_exception import RepositoryException
from src.model.db_schema.transaction_vew_schema import TransactionViewSchema
from src.core.di import ioc

@ioc.register
class TransactionViewRepository:
    def get_all(self) -> list[TransactionViewSchema]|iter[TransactionViewSchema]:
        try:
            with SessionLocal() as session:
                entities = session.query(TransactionView).all()
            return [TransactionViewSchema.model_validate(entity) for entity in entities]
        except Exception as e:
            raise RepositoryException(f"Error fetching all transaction views: {str(e)}")
    
    def get(self, id: int) -> TransactionViewSchema:
        try:
            with SessionLocal() as session:
                entity = session.get(TransactionView, id)
            if entity is None:
                raise RepositoryException(f"Transaction view with ID {id} not found")
            return TransactionViewSchema.model_validate(entity)
        except Exception as e:
            raise RepositoryException(f"Error fetching transaction view with ID {id}: {str(e)}")