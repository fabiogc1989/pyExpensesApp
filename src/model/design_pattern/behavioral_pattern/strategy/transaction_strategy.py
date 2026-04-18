from abc import ABC, abstractmethod
from typing import override

from src.core.di import Inject
from src.model.db_schema.credit_schema import CreditSchema
from src.model.db_schema.debit_schema import DebitSchema
from src.repository.credit_repository import CreditRepository
from src.repository.debit_repository import DebitRepository


class TransactionScreenContext:
    __strategy: TransactionStrategy = None
    
    def set_strategy(self, strategy: TransactionStrategy):
        self.__strategy = strategy
    
    def save(self, data: dict):
        self.__strategy.save(data)


class TransactionStrategy(ABC):
    @abstractmethod
    def save(self, data: dict):
        ...


class DebitStrategy(TransactionStrategy):
    repo = Inject(DebitRepository)

    @override
    def save(self, data: dict):
        entity = DebitSchema(**data)
        self.repo.insert(entity)
    

class CreditStrategy(TransactionStrategy):
    repo = Inject(CreditRepository)

    @override
    def save(self, data: dict):
        entity = CreditSchema(**data)
        self.repo.insert(entity)