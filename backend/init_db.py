"""
Initialize the database and create tables
"""
from utils.database import Base, engine
from utils.models import User, Project, RoadmapStep

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
