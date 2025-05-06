from fastapi import FastAPI, Request
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

from utils.models import Base, Project
from utils.database import engine, SessionLocal, get_db
from routers.auth import router as auth_router
from routers.project import router as project_router
from routers.user import router as user_router

import os


app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_DIR = os.path.join(BASE_DIR, "static")
# app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/explore", status_code=status.HTTP_200_OK) # Project get/query
async def get_public_ideas(request: Request, 
                    db: db_dependency): 
    # fotoğraflar static/uploads içerisinde bulunuyor
    # only public projects will be returned

    public_projects = db.query(Project).filter(Project.is_public == True).all()
    if not public_projects:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No public projects found")
    return JSONResponse(content=public_projects)


@app.get("/explore/{keyword}", status_code=status.HTTP_200_OK)
async def search_public_ideas(request: Request, db: db_dependency, keyword: str):
    pass 

