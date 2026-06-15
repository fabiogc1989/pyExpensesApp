from typing import cast

from src.core.di import Inject, ioc
from src.model.transaction import Transaction
from src.model.transaction_search import TransactionInputSearch, TransactionSearch
from src.model.transaction_type import TransactionType
from src.repository.bank_account_repository import BankAccountRepository
from src.repository.credit_repository import CreditRepository
from src.repository.debit_repository import DebitRepository
from src.repository.transaction_view_repository import TransactionViewRepository


@ioc.register
class TransactionService:
    __bank_account_repo: BankAccountRepository = cast(
        BankAccountRepository, Inject(BankAccountRepository)
    )
    __transaction_view_repo: TransactionViewRepository = cast(
        TransactionViewRepository, Inject(TransactionViewRepository)
    )
    __credit_repo: CreditRepository = cast(CreditRepository, Inject(CreditRepository))
    __debit_repo: DebitRepository = cast(DebitRepository, Inject(DebitRepository))

    def get_search_model(self) -> TransactionInputSearch:
        bank_accounts = self.__bank_account_repo.get_all()
        model = TransactionInputSearch(
            ibanList=[bank_account.iban for bank_account in bank_accounts]
        )
        return model

    def search_transactions(self, search_model: TransactionSearch) -> list[Transaction]:
        data = self.__transaction_view_repo.search_transactions(search_model)
        return [
            Transaction(
                row_number=item.unique_row_id,
                transaction_id=item.id,
                description=item.description,
                amount=item.amount,
                date=item.date,
                type=TransactionType[item.type],
                iban=item.bank_account.iban,
            )
            for item in data
        ]

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
