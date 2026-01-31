from models.base import Base
from models.debit import Debit
from models.credit import Credit
from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BankAccount(Base):
    __tablename__ = 'bank_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    iban: Mapped[str] = mapped_column(String(34), nullable=False)
    debits: Mapped[List['Debit']] = relationship(back_populates='bank_account')
    credits: Mapped[List['Credit']] = relationship(back_populates='bank_account')