from abc import ABC, abstractmethod
from typing import cast, override

from src.core.di import Inject
from src.model.db_schema.credit_schema import CreditSchema
from src.model.db_schema.debit_schema import DebitSchema
from src.repository.credit_repository import CreditRepository
from src.repository.debit_repository import DebitRepository


class TransactionStrategy(ABC):
    @abstractmethod
    def save(self, data: dict): ...


class TransactionScreenContext:
    __strategy: TransactionStrategy

    def set_strategy(self, strategy: TransactionStrategy):
        self.__strategy = strategy

    def save(self, data: dict):
        self.__strategy.save(data)


class DebitStrategy(TransactionStrategy):
    __repo: DebitRepository = cast(DebitRepository, Inject(DebitRepository))

    @override
    def save(self, data: dict):
        entity = DebitSchema(**data)
        self.__repo.insert(entity)


class CreditStrategy(TransactionStrategy):
    __repo: CreditRepository = cast(CreditRepository, Inject(CreditRepository))

    @override
    def save(self, data: dict):
        entity = CreditSchema(**data)
        self.__repo.insert(entity)
