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

<<<<<<< HEAD
from utils.database import Base
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
=======
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel, ConfigDict
from typing import List
import re
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9

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

<<<<<<< HEAD
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
=======
    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey('users.id'))
    title           = Column(String) # project name
    description     = Column(String) # project short description
    materials       = Column(String) # project materials
    roadmap         = Column(String) # project steps
    image           = Column(String) # recyclable item image
    created_at      = Column(String)
    recycled_image  = Column(String, default=None) # recycled item image
    is_public       = Column(Boolean, default=False)


class ProjectSchema(BaseModel):
    id: int
    user_id: int
    image: str
    title: str
    description: str
    materials: str
    roadmap: str
    created_at: str
    recycled_image: str | None
    is_public: bool

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def _decode_field(value: str) -> List[str]:
        list_ = value.split("-")
        list_ = [item.replace("{", "") for item in list_]
        list_ = [item.replace("}", "") for item in list_]
        return list_

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        data["materials"] = self._decode_field(self.materials)
        data["roadmap"] = self._decode_field(self.roadmap)
        return data

>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
