from datetime import date

from pydantic import BaseModel, ConfigDict

from src.model.db_schema.bank_account_schema import BankAccountSchema


class TransactionViewSchema(BaseModel):
    unique_row_id: int
    id: int
    description: str
    amount: float
    date: date
    type: str
    bank_account_id: int
    bank_account: BankAccountSchema

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)
