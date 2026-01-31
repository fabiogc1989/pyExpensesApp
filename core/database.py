from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base


# 1. Define the database location (SQLite will create a local file)
DB_URL = "sqlite+pysqlite:///data/expenses.db"

# 2. Create the Engine (the connection engine)
# 'check_same_thread=False' is required on SQLite to work well with Tkinter
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

# 3. Create a session factory
# Each time we call SessionLocal(), we get a new session with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create the database tables if they don't exist."""
    # Import models here to ensure `Base` is aware of them
    import models
    Base.metadata.create_all(bind=engine)