from enum import IntEnum


class TransactionType(IntEnum):
    DEBIT = 0
    CREDIT = 1


TransactionTypeValues = {
    'DEBIT': TransactionType.DEBIT,
    'CREDIT': TransactionType.CREDIT
}