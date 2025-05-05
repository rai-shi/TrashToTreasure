<<<<<<< HEAD
from fastapi import FastAPI, Request, Depends, File, UploadFile, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import timedelta
from services.project_service import ProjectService
from pydantic import BaseModel
import uvicorn
import os
import requests

from utils.database import get_db, engine, Base
from utils.models import User
from utils.auth import (CreateUserRequest, LoginRequest, get_password_hash, verify_password,
                     create_access_token, authenticate_user, verify_token, get_user_by_id)

# Create database tables
Base.metadata.create_all(bind=engine)
=======
from fastapi import FastAPI, Request
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from utils.models import Base, Project
from utils.database import engine, SessionLocal, get_db
from routers.auth import router as auth_router
from routers.project import router as project_router
from routers.user import router as user_router
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9

import os


app = FastAPI()

<<<<<<< HEAD
# Project request models
class CreateProjectRequest(BaseModel):
    name: str
    description: str

# CORS ayarları - Tüm kaynaklara izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

GEMINI_API_KEY = "AIzaSyABndYh8Iw2s4K1NpYVKVAtXxpdc-0pLx0"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

@app.get("/")
def read_root():
    return {"message": "TrashToTreasure API is running"}

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is healthy"}

@app.post("/auth/register")
async def register(user_data: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        # Kullanıcı adı veya email zaten var mı kontrol et
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | 
            (User.email == user_data.email)
        ).first()
        
        if existing_user:
            return JSONResponse(
                status_code=400,
                content={"detail": "Username or email already exists"}
            )
        
        # Yeni kullanıcı oluştur
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    except Exception as e:
        print(f"Kayıt hatası: {str(e)}")
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal error: {str(e)}"}
        )
        
@app.post("/auth/login")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, login_data.username, login_data.password)
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Incorrect username or password"}
            )
        
        access_token = create_access_token(
            username=user.username,
            user_id=user.id,
            expire_time=timedelta(minutes=30)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id
        }
    except Exception as e:
        print(f"Giriş hatası: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal error: {str(e)}"}
        )

@app.get("/user/profile")
async def get_profile(request: Request, db: Session = Depends(get_db)):
    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )
        
        # Get token
        token = auth_header.split(' ')[1]
        
        # Verify token
        token_data = verify_token(token)
        if not token_data:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
        
        # Get user from database
        user = get_user_by_id(db, token_data['user_id'])
        
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
    except Exception as e:
        print(f"Profil hata oluştu: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal error: {str(e)}"}
        )

@app.get("/user/projects")
async def get_user_projects(request: Request, db: Session = Depends(get_db)):
    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )
        
        # Get token
        token = auth_header.split(' ')[1]
        
        # Verify token
        token_data = verify_token(token)
        if not token_data:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
            
        # Get user projects from service
        service = ProjectService(db)
        projects = service.get_user_projects(token_data['user_id'])
        
        return projects
    except Exception as e:
        print(f"Projects error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal error: {str(e)}"}
        )

# Direkt çalıştırma
@app.post("/projects")
async def create_project(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    print("[DEBUG] Starting project creation...")
    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            print("[DEBUG] Missing or invalid authorization header")
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )
        
        token = auth_header.split(' ')[1]
        token_data = verify_token(token)
        
        if not token_data:
            print("[DEBUG] Invalid token")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
            
        print(f"[DEBUG] User authenticated: {token_data['user_id']}")
        
        # Validate image
        if not image.content_type.startswith('image/'):
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid file type. Please upload an image."}
            )
        
        # Read image data
        print("[DEBUG] Reading image data...")
        image_data = await image.read()
        
        if not image_data:
            return JSONResponse(
                status_code=400,
                content={"detail": "Empty image file"}
            )
        
        # Create project and generate roadmap
        print("[DEBUG] Creating project and generating roadmap...")
        service = ProjectService(db)
        project = await service.create_project_with_roadmap(
            user_id=token_data['user_id'],
            name=name,
            description=description,
            image_data=image_data
        )
        
        print(f"[DEBUG] Project created successfully with ID: {project.id}")
        return {"project_id": project.id}
        
    except Exception as e:
        print(f"[ERROR] Project creation failed: {str(e)}")
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Project creation failed: {str(e)}"}
        )

@app.get("/projects/{project_id}/roadmap")
async def get_project_roadmap(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Get user from token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )
        
        token = auth_header.split(' ')[1]
        token_data = verify_token(token)
        
        if not token_data:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
        
        # Get project roadmap
        service = ProjectService(db)
        roadmap = service.get_project_roadmap(project_id)
        
        return roadmap
        
    except Exception as e:
        print(f"Roadmap fetch error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal error: {str(e)}"}
        )

@app.get("/projects/{project_id}")
async def get_project_details(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )
        
        token = auth_header.split(' ')[1]
        token_data = verify_token(token)
        
        if not token_data:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
        
        # Get project details
        service = ProjectService(db)
        project = service.get_project_details(project_id)
        
        if not project:
            return JSONResponse(
                status_code=404,
                content={"detail": "Project not found"}
            )
            
        # Check if user has access to this project
        if project['user_id'] != token_data['user_id'] and not project['is_public']:
            return JSONResponse(
                status_code=403,
                content={"detail": "You don't have permission to view this project"}
            )
        
        return project
        
    except Exception as e:
        print(f"Project details error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal error: {str(e)}"}
        )

@app.get("/dev/reset-db")
async def dev_reset_db():
    """
    Development endpoint to recreate database tables.
    This should be disabled in production.
    """
    try:
        # Drop all tables and recreate them
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        return {"message": "Database reset successfully"}
    except Exception as e:
        print(f"Database reset error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Database reset error: {str(e)}"}
        )

@app.post("/api/gemini")
async def gemini_chat(prompt: str = Body(..., embed=True)):
    try:
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        response.raise_for_status()
        gemini_data = response.json()
        # Cevabı metin olarak döndür
        text = gemini_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return {"response": text}
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": f"Gemini API error: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
=======
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_DIR = os.path.join(BASE_DIR, "static")
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/explore-ideas", status_code=status.HTTP_200_OK) # Project get/query
async def get_public_ideas(request: Request, 
                    db: db_dependency): 
    # fotoğraflar static/uploads içerisinde bulunuyor
    # only public projects will be returned

    public_projects = db.query(Project).filter(Project.is_public == True).all()
    if not public_projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No public projects found")
    return JSONResponse(content=public_projects)


@app.get("/explore-ideas/{keyword}", status_code=status.HTTP_200_OK)
async def search_public_ideas(request: Request, db: db_dependency, keyword: str):
    pass 
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
