from models.base import Base
from models.bank_account import BankAccount
from datetime import date
from sqlalchemy import ForeignKey, func, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Debit(Base):
    __tablename__ = 'debit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped["BankAccount"] = relationship(back_populates='debits')