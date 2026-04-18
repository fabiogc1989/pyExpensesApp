from src.core.di import Inject, ioc
from src.model.transaction import Transaction
from src.model.transaction_type import TransactionType, TransactionTypeValues
from src.repository.credit_repository import CreditRepository
from src.repository.debit_repository import DebitRepository
from src.repository.transaction_view_repository import TransactionViewRepository

@ioc.register
class TransactionService:
    __transaction_view_repo: TransactionViewRepository = Inject(TransactionViewRepository)
    __credit_repo: CreditRepository = Inject(CreditRepository)
    __debit_repo: DebitRepository = Inject(DebitRepository)

    def search_transactions(self) -> list[Transaction]:
        data = self.__transaction_view_repo.get_all()
        return [Transaction(
            row_number=item.unique_row_id, 
            transaction_id=item.id, 
            description=item.description, 
            amount=item.amount, 
            date=item.date, 
            type=TransactionTypeValues.get(item.type), 
            iban=item.bank_account.iban
        ) for item in data]
    
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