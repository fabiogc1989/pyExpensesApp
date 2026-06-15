from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from src.model.transaction_type import TransactionType


class TransactionCreation(BaseModel):
    description: Optional[str] = None
    amount: float
    date: date
    type: TransactionType
    bank_account_id: int

    model_config = ConfigDict(validate_assignment=True)

    @field_validator('amount')
    @classmethod
    def amount_must_Be_non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Amount must be a non-negative number.')
        return v

    @field_validator('date')
    @classmethod
    def date_must_not_be_in_the_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Date cannot be in the future.')
        return v

    @field_validator('type')
    @classmethod
    def type_must_be_valid(cls, v: TransactionType) -> TransactionType:
        if not v:
            raise ValueError('Transaction type is required.')
        return v

    @field_validator('bank_account_id')
    @classmethod
    def bank_account_id_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Bank account ID must be a positive integer.')
        return v
