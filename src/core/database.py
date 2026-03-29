from datetime import date
from typing import List
from sqlalchemy import create_engine, String, Date, ForeignKey, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


# 1. Define the database location (SQLite will create a local file)
DB_URL = "sqlite+pysqlite:///data/expenses.db"

# 2. Create the Engine (the connection engine)
# 'check_same_thread=False' is required on SQLite to work well with Tkinter
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# 3. Create a session factory
# Each time we call SessionLocal(), we get a new session with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4. Define the database models
class Base(DeclarativeBase):
    pass


class BankAccount(Base):
    __tablename__ = 'bank_account'

    id: Mapped[int] = mapped_column(primary_key=True)
    iban: Mapped[str] = mapped_column(String(34), nullable=False)
    
    debits: Mapped[List[Debit]] = relationship('Debit', back_populates='bank_account')
    credits: Mapped[List[Credit]] = relationship('Credit', back_populates='bank_account')


class Credit(Base):
    __tablename__ = 'credit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped[BankAccount] = relationship('BankAccount', back_populates='credits')


class Debit(Base):
    __tablename__ = 'debit'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.now())
    
    bank_account_id: Mapped[int] = mapped_column(ForeignKey('bank_account.id'), nullable=False)
    bank_account: Mapped[BankAccount] = relationship('BankAccount', back_populates='debits')


# 5. Create the database tables
def init_db():
    """Create the database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)