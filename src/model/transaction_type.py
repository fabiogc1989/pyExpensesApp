from enum import Enum


class TransactionType(Enum):
    ALL = None
    DEBIT = 0
    CREDIT = 1


TransactionTypeValues = {
    'DEBIT': TransactionType.DEBIT,
    'CREDIT': TransactionType.CREDIT,
    'ALL': TransactionType.ALL
}