from datetime import date
from pydantic import BaseModel

from src.model.transaction_type import TransactionType


class TransactionSearch(BaseModel):
    min_amount: float | None = None
    max_amount: float | None = min_amount
    start_date: date | None = None
    end_date: date | None = start_date
    description: str | None = None
    type: TransactionType | None = None