from src.core.di import Inject
from src.repository.credit_repository import CreditRepository
from src.repository.debit_repository import DebitRepository
from src.repository.transaction_view_repository import TransactionViewRepository


class TransactionService:
    __transaction_view_repo: TransactionViewRepository = Inject(TransactionViewRepository)
    __credit_repo: CreditRepository = Inject(CreditRepository)
    __debit_repo: DebitRepository = Inject(DebitRepository)

    def search_transactions(self):
        return self.__transaction_view_repo.get_all()
    
    def add_transaction(self, item):
        if item['type'] == 'credit':
            self.__credit_repo.insert(item)
        elif item['type'] == 'debit':
            self.__debit_repo.insert(item)
        else:
            raise ValueError("Invalid transaction type. Must be 'credit' or 'debit'.")
        
    def update_transaction(self, item):
        if item['type'] == 'credit':
            self.__credit_repo.update(item)
        elif item['type'] == 'debit':
            self.__debit_repo.update(item)
        else:
            raise ValueError("Invalid transaction type. Must be 'credit' or 'debit'.")
        
    def delete_transaction(self, item):
        if item['type'] == 'credit':
            self.__credit_repo.delete(item)
        elif item['type'] == 'debit':
            self.__debit_repo.delete(item)
        else:
            raise ValueError("Invalid transaction type. Must be 'credit' or 'debit'.")