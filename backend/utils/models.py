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

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel, ConfigDict
from typing import List
import re

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

