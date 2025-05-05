"""
User
- id: int
- username: str
- email: str
- first_name: str
- last_name: str
- password: str

Project
- id: int
- name: str
- image: str
- description: str
- user_id: int
- created_at: datetime
- updated_at: datetime
- done: bool
- is_public: bool
"""

from utils.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)

class Project(Base):
    __tablename__ = 'project'

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey('users.id'))
    name            = Column(String) # project name
    description     = Column(String) # project short description
    roadmap         = Column(String) # project steps
    image           = Column(String) # recyclable item image
    created_at      = Column(String)
    # recycled_image  = Column(String, default="") # recycled item image
    # is_public       = Column(Boolean, default=False)