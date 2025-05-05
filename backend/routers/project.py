"""
get_recyclable_item_image
get_materials
create_ideas
get_roadmap
"""
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session

from starlette import status
from starlette.responses import RedirectResponse
from utils.models import Base, Project
from utils.database import engine, SessionLocal
from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi import UploadFile, File, Body
from fastapi.responses import JSONResponse
from fastapi import Form

from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import os


import google.generativeai as genai

import uuid
import aiofiles

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import markdown
from bs4 import BeautifulSoup

from utils.database import SessionLocal, get_db
from utils.models import User, Base, Project, ProjectSchema
from utils.auth import *


BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BACKEND_DIR)
STATIC_DIR = os.path.join(BASE_DIR, "static")


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)

class EditRequest(BaseModel):
    recycled_image: str
    is_public: bool = Field(default=False)

class IdeaRequest(BaseModel):
    image_path: str
    title: str
    description: str
    materials: List[str]
    roadmap: List[str]


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_token)]

# yapılacak
def ask_gemini(image):
    example = [
        {
            "name": "Kalemlik",
            "description": "Kullanılmayan bardağı bir kalemliğe dönüştürün.",
            "materials": ["Cam Boyası"],
            "roadmap": [
                "Bardağı temizleyin.",
                "Cam boyası ile bardağı boyayın.",
                "Bardak kuruduktan sonra kalemlerinizi yerleştirin."
            ]
        },
        {
            "name": "Gece Lambası",
            "description": "Kullanılmayan bardağı gece lambası yapın.",
            "materials": ["LED ışık", "Kablo", "Mukavva"],
            "roadmap": [
                "Bardağı temizleyin.",
                "Mukavvadan bir taban kesin.",
                "LED ışığını bardağa yerleştirin.",
                "Mukavvayı bardağın altına yapıştırın.",
                "LED ışığını bir güç kaynağına bağlayın.",
                "Bardağı bir lamba olarak kullanın."
            ]
        }
    ]
    return example

async def save_image(image: UploadFile):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Sadece JPG veya PNG dosyaları kabul edilir.")

    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(STATIC_DIR, "uploads", unique_filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)

    print(f"Image saved to {file_path}")

    return file_path


# yapılacak
@router.post("/create-ideas", status_code=status.HTTP_200_OK)
async def get_recycle_ideas( 
                    request: Request,
                    user:user_dependency,
                    db: db_dependency,
                    image: UploadFile = File(...),
                    # title: str = Form(...),
                    # description: str = Form(...),
                ): 
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        if verified_user is None:
            return redirect_to_login()
    except:
        return redirect_to_login()
    
    image_path = await save_image(image)
    print(image_path)
    
    """
    get image from request
    save it to static/uploads
    ask gemini to return ideas in format of
        project name
        short project description
        required materials
        project steps 

    tüm dönen bilgileri bir json objesi olarak döndürürüz
    kullanıcı bir proje fikri seçtiğinde
    geri dönüşüm fikri ikinci onaydan geçerse bize ajax onayı döner 
    ve biz de bu projeyi veritabanına kaydederiz
    """
                    
    ideas = ask_gemini(image)
    print(ideas)

    content = {
        "image": image_path,
        "ideas": ideas
    }
    
    return JSONResponse(content=content)
    

# system prompt
"""
You are an assistant that generates upcycling DIY project ideas from an item image.

Return your response strictly as a JSON array. Each element must have:
- title (string)
- description (string)
- materials (list of strings)
- roadmap (list of step strings)

Example format:
[
  {
    "title": "Project Name",
    "description": "Project short description",
    "materials": ["Material 1", "Material 2"],
    "roadmap": [
        "Step 1",
        "Step 2",
        "Step 3"
    ]
  }
]

Input will be an image of a recyclable item.
Respond have to be only in the above JSON format.
"""
# User Prompt → "Here is an image of a used t-shirt. Give me 3 ideas."
# Image Input → modele ayrı olarak verilir


@router.post("/save-idea", status_code=status.HTTP_201_CREATED)
async def save_selected_idea(
                            request: Request,
                            user: user_dependency,
                            db: db_dependency,
                            idea: IdeaRequest
                        ):
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        if verified_user is None:
            return redirect_to_login()
        
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
    except:
        return redirect_to_login()


    new_project = Project(
        user_id     = user.id,
        image       = idea.image_path,
        title       = idea.title,
        description = idea.description,
        materials   = "-".join([f"{{{item}}}" for item in idea.materials]),
        roadmap     = "-".join([f"{{{item}}}" for item in idea.roadmap]), 
        created_at  = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    print(new_project)

    return RedirectResponse(
        url=f"/project/my-ideas/{new_project.id}",
        status_code=status.HTTP_302_FOUND)
    
@router.get("/my-ideas", status_code=status.HTTP_200_OK) # get all projects
async def get_ideas(
                    request: Request, 
                    user: user_dependency,
                    db: db_dependency):
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        if verified_user is None:
            return redirect_to_login()
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
    except:
        return redirect_to_login()
        
    items = db.query(Project).filter(Project.user_id == user.id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No projects found")
    
    response_data = [ ProjectSchema.model_validate(item).model_dump() for item in items ]
    return JSONResponse(content=response_data)

@router.get("/my-ideas/{item_id}", status_code=status.HTTP_200_OK) # Project get
async def get_idea(
                    request: Request,
                    user: user_dependency,
                    db: db_dependency,
                    item_id: int):
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        if verified_user is None:
            return redirect_to_login()
        
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
    except:
        return redirect_to_login()
    item = db.query(Project).filter(Project.id == item_id).filter(Project.user_id == user.id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    response_data = ProjectSchema.model_validate(item).model_dump() 
    return JSONResponse(content=response_data)




@router.put("/my-ideas/{item_id}", status_code=status.HTTP_201_CREATED) # Project update/edit
async def edit_idea(
                    request: Request,
                    user: user_dependency,
                     db: db_dependency, 
                     item_id: int, 
                     edit_request: EditRequest):
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        if verified_user is None:
            return redirect_to_login()
        
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
    except:
        return redirect_to_login()
    
    item = db.query(Project).filter(Project.id == item_id).filter(Project.user_id == user.id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    item.recycled_image = edit_request.recycled_image
    item.is_public = edit_request.is_public
    db.add(item)
    db.commit()
    db.refresh(item)
    return JSONResponse(content=item)

# what is delete status code

@router.delete("/my-ideas/{item_id}", status_code=status.HTTP_204_NO_CONTENT) # Project delete
async def delete_idea(
                request: Request,
                user: user_dependency,
                db: db_dependency, 
                item_id:int):
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        if verified_user is None:
            return redirect_to_login()
        
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
    except:
        return redirect_to_login()
    
    item = db.query(Project).filter(Project.id == item_id).filter(Project.user_id == user.id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    else:
        db.delete(item)
        db.commit()