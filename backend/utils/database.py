from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


current_directory = os.path.dirname(os.path.abspath(__file__)) # utils directory, routers
backend_directory = os.path.dirname(current_directory) # backend directory

environment_path = backend_directory + "/.env"

load_dotenv(environment_path)

SQLALCHAMY_DATABASE_URL = os.getenv("SQLALCHAMY_DATABASE_URL")

engine = create_engine(
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


