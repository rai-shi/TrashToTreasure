from sqlalchemy import create_engine
<<<<<<< HEAD
from sqlalchemy.orm import Session, DeclarativeBase
from typing import Generator
=======
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
import os
import sys

<<<<<<< HEAD
class Base(DeclarativeBase):
    pass
=======

current_directory = os.path.dirname(os.path.abspath(__file__)) # utils directory, routers
backend_directory = os.path.dirname(current_directory) # backend directory

environment_path = backend_directory + "/.env"

load_dotenv(environment_path)

SQLALCHAMY_DATABASE_URL = os.getenv("SQLALCHAMY_DATABASE_URL")
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9

# Database path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Database directory: {BASE_DIR}")
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'trashtotreasure.db')}"
print(f"Database URL: {DATABASE_URL}")

# Create SQLite engine
engine = create_engine(
<<<<<<< HEAD
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
=======
    SQLALCHAMY_DATABASE_URL, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9


