from datetime import date
from pydantic import BaseModel, ConfigDict

class TransactionViewSchema(BaseModel):
    unique_row_id: int
    id: int
    description: str
    amount: float
    date: date
    type: str
    bank_account_id: int

    # This allows Pydantic to read SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )
    