from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class BankAccountSchema(BaseModel):
    id: Optional[int] = None
    iban: str

    model_config = ConfigDict(
        from_attributes=True,  # This allows Pydantic to read SQLAlchemy models
        validate_assignment=True,
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
