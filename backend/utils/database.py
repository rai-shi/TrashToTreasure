from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from typing import Generator
import os
import sys

class Base(DeclarativeBase):
    pass

# Database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Database directory: {BASE_DIR}")
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'trashtotreasure.db')}"
print(f"Database URL: {DATABASE_URL}")

# Create SQLite engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

def get_db() -> Generator[Session, None, None]:
    """Get a database session"""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            print(f"Database error: {str(e)}", file=sys.stderr)
            session.rollback()
            raise


