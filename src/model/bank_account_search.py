from typing import Optional

from pydantic import BaseModel


class BankAccountSearch(BaseModel):
    iban: Optional[str] = None
