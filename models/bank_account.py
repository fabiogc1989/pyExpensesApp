from datetime import date
from models.base import Base
from typing import List
from sqlalchemy import String, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BankAccount(Base):
    __tablename__ = 'bank_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    iban: Mapped[str] = mapped_column(String(34), nullable=False)
    
    debits: Mapped[List['Debit']] = relationship('Debit', back_populates='bank_account')
    credits: Mapped[List['Credit']] = relationship('Credit', back_populates='bank_account')


class Credit(Base):
    __tablename__ = 'credit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped['BankAccount'] = relationship('BankAccount', back_populates='credits')


class Debit(Base):
    __tablename__ = 'debit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped['BankAccount'] = relationship('BankAccount', back_populates='debits')