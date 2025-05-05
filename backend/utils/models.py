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
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    
    # Relationships
    projects: Mapped[List["Project"]] = relationship(back_populates="user")

class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()  # Base64 encoded image
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    done: Mapped[bool] = mapped_column(default=False)
    is_public: Mapped[bool] = mapped_column(default=False)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="projects")
    roadmap_steps: Mapped[List["RoadmapStep"]] = relationship(back_populates='project', cascade="all, delete-orphan")

class RoadmapStep(Base):
    __tablename__ = 'roadmap_steps'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    step_number: Mapped[int] = mapped_column()
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    estimated_time: Mapped[str] = mapped_column()
    materials_needed: Mapped[dict] = mapped_column(type_=JSON)  # Store as JSON array
    
    # Relationships
    project: Mapped["Project"] = relationship(back_populates='roadmap_steps')