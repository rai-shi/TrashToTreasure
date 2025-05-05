"""
API endpoints for projects:
- get_projects
- get_project
- create_project
- create_ideas
"""
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Path, HTTPException, Request, UploadFile, File, Form
from dotenv import load_dotenv
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import markdown
from bs4 import BeautifulSoup
from utils.models import Project, User
from utils.database import get_db
from utils.auth import verify_token


# API modelleri
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    image: str
    user_id: int

class ProjectCreateRequest(BaseModel):
    name: str
    description: str

class IdeaResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_token)]

@router.get("/explore", response_model=List[ProjectResponse])
async def get_projects(db: db_dependency):
    """
    Get all projects
    """
    # Örnek proje verileri döndürüyoruz
    # Gerçek uygulamada veritabanından çekilecek
    return [
        {
            "id": 1,
            "name": "Şişe Lamba",
            "description": "Eski cam şişeleri dekoratif lambalara dönüştürün.",
            "image": "https://via.placeholder.com/300x200?text=Sise+Lamba",
            "user_id": 1
        },
        {
            "id": 2,
            "name": "Palet Sehpa",
            "description": "Atık ahşap paletlerden şık bir sehpa yapımı.",
            "image": "https://via.placeholder.com/300x200?text=Palet+Sehpa",
            "user_id": 2
        },
        {
            "id": 3,
            "name": "T-Shirt Çanta",
            "description": "Eski tişörtlerinizden dikişsiz alışveriş çantası yapın.",
            "image": "https://via.placeholder.com/300x200?text=Tisort+Canta",
            "user_id": 1
        }
    ]

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: db_dependency):
    """
    Get project by id
    """
    # Gerçek uygulamada veritabanından ID'ye göre proje çekilecek
    return {
        "id": project_id,
        "name": "Örnek Proje",
        "description": "Bu bir örnek projedir",
        "image": "https://via.placeholder.com/300x200?text=Ornek+Proje",
        "user_id": 1
    }

@router.post("/create", response_model=ProjectResponse)
async def create_project(
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    user: user_dependency = None,
    db: db_dependency = None
):
    """
    Create a new project
    """
    # Gerçek uygulamada dosya kaydedilip veritabanına proje eklenecek
    
    # Şu an için sadece örnek bir yanıt döndürüyoruz
    return {
        "id": 10,
        "name": name,
        "description": description,
        "image": "https://via.placeholder.com/300x200?text=Yeni+Proje",
        "user_id": user["user_id"] if user else 1
    }

@router.post("/ideas", response_model=List[IdeaResponse])
async def generate_ideas(
    item_description: str = Form(...),
    image: Optional[UploadFile] = File(None),
    user: user_dependency = None
):
    """
    Generate recycling ideas for an item
    """
    # Gerçek uygulamada Google GenAI API'si kullanılabilir
    
    # Şu an için sabit veriler döndürüyoruz
    return [
        {
            "id": 1,
            "title": "Dekoratif Vazo",
            "description": "Temizlendikten sonra cam boyasıyla renklendirilip dekoratif bir vazoya dönüştürülebilir.",
            "difficulty": "Kolay"
        },
        {
            "id": 2,
            "title": "LED Lamba",
            "description": "İçine LED ışık dizisi yerleştirilerek şık bir gece lambası yapılabilir.",
            "difficulty": "Orta"
        },
        {
            "id": 3,
            "title": "Bahçe Süsü",
            "description": "Renkli camlarla kaplanarak bahçe için dekoratif bir süs oluşturulabilir.",
            "difficulty": "Zor"
        }
    ]