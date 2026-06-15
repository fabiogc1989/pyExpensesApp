from datetime import date

from pydantic import BaseModel

from .transaction_type import TransactionType


class Transaction(BaseModel):
    row_number: int
    transaction_id: int
    description: str
    amount: float
    date: date
    type: TransactionType
    iban: str
