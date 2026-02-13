from datetime import date
from pydantic import BaseModel, ConfigDict


class BankAccountSchema(BaseModel):
    id: int
    iban: str

    # Here's the magic: Pydantic converts the list of objects from SQL
    debits: list[DebitSchema] = []
    credits: list[CreditSchema] = []

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


class CreditSchema(BaseModel):
    id: int
    description: str
    amount: float
    date: date

    # Here's the magic: Pydantic converts the BankAccount object from SQL
    bank_account: BankAccountSchema

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


class DebitSchema(BaseModel):
    id: int
    description: str
    amount: float
    date: date

    # Here's the magic: Pydantic converts the BankAccount object from SQL
    bank_account: BankAccountSchema

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)