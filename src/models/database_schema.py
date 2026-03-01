from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class BankAccountSchema(BaseModel):
    id: Optional[int] = None
    iban: str

    # Here's the magic: Pydantic converts the list of objects from SQL
    debits: list[DebitSchema] = []
    credits: list[CreditSchema] = []

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

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


class CreditSchema(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    date: date

    # Here's the magic: Pydantic converts the BankAccount object from SQL
    bank_account: BankAccountSchema

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


class DebitSchema(BaseModel):
    id: Optional[int] = None
    description: str
    amount: float
    date: date

    # Here's the magic: Pydantic converts the BankAccount object from SQL
    bank_account: BankAccountSchema

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)