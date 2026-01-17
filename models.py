from datetime import date
from typing import List
from sqlalchemy import ForeignKey, func, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class BankAccount(Base):
    __tablename__ = 'bank_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    iban: Mapped[str] = mapped_column(String(34), nullable=False)
    debits: Mapped[List['Debit']] = relationship(back_populates='bank_account')
    credits: Mapped[List['Credit']] = relationship(back_populates='bank_account')


class Debit(Base):
    __tablename__ = 'debit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped["BankAccount"] = relationship(back_populates='debits')


class Credit(Base):
    __tablename__ = 'credit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped["BankAccount"] = relationship(back_populates='credits')
