from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class CreditSchema(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    date: date
    bank_account_id: int

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: int) -> int:
        if v < 0:
            raise ValueError('ID must be a non-negative integer.')
        return v
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Amount must be a non-negative number.')
        return v
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Date cannot be in the future.')
        return v
    
    @field_validator('bank_account_id')
    @classmethod
    def validate_bank_account_id(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Bank account ID must be a non-negative integer.')
        return v


class DebitSchema(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    date: date
    bank_account_id: int

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: int) -> int:
        if v < 0:
            raise ValueError('ID must be a non-negative integer.')
        return v
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Amount must be a non-negative number.')
        return v
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Date cannot be in the future.')
        return v
    
    @field_validator('bank_account_id')
    @classmethod
    def validate_bank_account_id(cls, v: int) -> int:
        if v < 0:
            raise ValueError('Bank account ID must be a non-negative integer.')
        return v


class BankAccountSchema(BaseModel):
    id: Optional[int] = None
    iban: str
    
    model_config = ConfigDict(
        from_attributes=True, # This allows Pydantic to read SQLAlchemy models
        validate_assignment=True
    )

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: int) -> int:
        if v < 0:
            raise ValueError('ID must be a non-negative integer.')
        return v

    @field_validator('iban')
    @classmethod
    def validate_iban(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('The IBAN cannot be empty or contain only spaces.')
        return v.upper()  # Convert to uppercase for consistency