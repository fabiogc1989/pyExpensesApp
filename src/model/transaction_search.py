from datetime import date
from typing import Optional
from pydantic import BaseModel

from src.model.transaction_type import TransactionType


class TransactionSearch(BaseModel):
    iban: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    type: TransactionType = TransactionType.ALL


class TransactionInputSearch(TransactionSearch):
    ibanList: list[str]