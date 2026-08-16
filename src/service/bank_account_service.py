from typing import cast

from src.core.di import Inject
from src.exception.repository_exception import RepositoryException
from src.model.bank_account_search import BankAccountSearch
from src.model.db_schema.bank_account_schema import BankAccountSchema
from src.repository.bank_account_repository import BankAccountRepository

from src.exception.service_exception import ServiceException

from src.core.di import ioc

@ioc.register
class BankAccountService:
    __bank_account_repo: BankAccountRepository = cast(
        BankAccountRepository, Inject(BankAccountRepository)
    )

    def get_all_bank_accounts(self) -> list[BankAccountSchema]:
        try:
            return self.__bank_account_repo.get_all()
        except RepositoryException as e:
            raise ServiceException(f'Failed to retrieve bank accounts:\n{str(e)}')
        except Exception as e:
            raise ServiceException(f'An unexpected error occurred while retrieving bank accounts:\n{str(e)}')

    def search_bank_account(self, search_model: BankAccountSearch) -> list[BankAccountSchema]:
        try:
            return self.__bank_account_repo.search_bank_accounts(search_model)
        except RepositoryException as e:
            raise ServiceException(f'Failed to search bank accounts:\n{str(e)}')
        except Exception as e:
            raise ServiceException(f'An unexpected error occurred while searching bank accounts:\n{str(e)}')

    def add_bank_account(self, item: BankAccountSchema):
        try:
            self.__bank_account_repo.insert(item)
        except RepositoryException as e:
            raise ServiceException(f'Failed to add bank account:\n{str(e)}')
        except Exception as e:
            raise ServiceException(f'An unexpected error occurred while adding bank account:\n{str(e)}')

    def update_bank_account(self, item: BankAccountSchema):
        try:
            self.__bank_account_repo.update(item)
        except RepositoryException as e:
            raise ServiceException(f'Failed to update bank account:\n{str(e)}')
        except Exception as e:
            raise ServiceException(f'An unexpected error occurred while updating bank account:\n{str(e)}')

    def delete_bank_account(self, id: int):
        try:
            self.__bank_account_repo.delete(id)
        except RepositoryException as e:
            raise ServiceException(f'Failed to delete bank account:\n{str(e)}')
        except Exception as e:
            raise ServiceException(f'An unexpected error occurred while deleting bank account:\n{str(e)}')