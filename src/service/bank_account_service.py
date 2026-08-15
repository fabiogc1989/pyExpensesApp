from typing import cast

from src.core.di import Inject
from src.model.bank_account_search import BankAccountSearch
from src.model.db_schema.bank_account_schema import BankAccountSchema
from src.repository.bank_account_repository import BankAccountRepository

from src.core.di import ioc

@ioc.register
class BankAccountService:
    __bank_account_repo: BankAccountRepository = cast(
        BankAccountRepository, Inject(BankAccountRepository)
    )

    def search_bank_account(self, search_model: BankAccountSearch) -> list[BankAccountSchema]:
        return self.__bank_account_repo.search_bank_accounts(search_model)

    def add_bank_account(self, item: BankAccountSchema):
        self.__bank_account_repo.insert(item)

    def update_bank_account(self, item: BankAccountSchema):
        self.__bank_account_repo.update(item)

    def delete_bank_account(self, id: int):
        self.__bank_account_repo.delete(id)