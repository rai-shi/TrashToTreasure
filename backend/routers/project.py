"""
get_recyclable_item_image
get_materials
create_ideas
get_roadmap
"""
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from starlette import status
from starlette.responses import RedirectResponse
from backend.utils.models import Base, Project
from backend.utils.database import engine, SessionLocal
from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi import UploadFile, File
from fastapi import Form
from fastapi.staticfiles import StaticFiles

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
from utils.models import User, Base
from utils.auth import *


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_token)]


@router.post("/recyclable-ideas",
             status_code=status.HTTP_200_OK)
async def get_recyclable_ideas(request: Request,
                               db: db_dependency,
                               user_: user_dependency,
                               file: UploadFile = File(...)):
    
    if file.content_type.startswith("image/"):
        image_bytes = await file.read()
        # görseli PIL ile açmak gerekebilir
        # image = Image.open(io.BytesIO(image_bytes))
    else:
        return JSONResponse(content={"error": "Invalid file type"}, status_code=400)

    # şimdilik eleyelim
    # eğer materials list varsa
    # if request.form.get("materials"):
    #     materials = request.form.get("materials")
    #     materials = materials.split(",")
    # else:
    #     materials = []
    
    # ask gemini to return ideas in specific format

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
    return JSONResponse(content=example)

# get image from request
# if material is exist, get them
# ask gemini to return ideas in format of
    # project name
    # short project description
    # required materials
    # project steps 

# tüm dönen bilgileri bir json objesi olarak döndürürüz
# kullanıcı bir proje fikri seçtiğinde
# geri dönüşüm fikri ikinci onaydan geçerse bize ajax onayı döner 
# ve biz de bu projeyi veritabanına kaydederiz


# system prompt
"""
You are an assistant that generates upcycling DIY project ideas from an item image.

Return your response strictly as a JSON array. Each element must have:
- name (string)
- description (string)
- materials (list of strings)
- roadmap (list of step strings)

Example format:
[
  {
    "name": "Project Name",
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

router.mount("/static", StaticFiles(directory="static"), name="static") # proje içerisinde 2 adet static klasörü var. Sonradan hata çıkartmaması için not aldım

class ItemRequest(BaseModel):
    title: str
    description: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=302) # adres doğru mu?
    redirect_response.delete_cookie("access_token")
    return redirect_response

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)] # get_current_user nerede?

@router.post("/add-item", status_code=status.HTTP_201_CREATED) # Project post
async def add_item(
    user: user_dependency,
    db: db_dependency,
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...)
):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Sadece JPG veya PNG dosyaları kabul edilir.")

    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = f"static/uploads/{unique_filename}"

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)

    item = Project(
        title=title,
        description=description,
        image=unique_filename,
        user_id = user.get('id')
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {"id": item.id, "title": item.title, "description": item.description, "image": item.image}

@router.put("/edit-items/{item_id}") # Project update/edit
async def edit_items(user:user_dependency, db: db_dependency, item_id: int, item_request: ItemRequest):
    item = db.query(Project).filter(item_id == Project.id).filter(Project.user_id == user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    item.title = item_request.title
    item.description = item_request.description
    db.add(item)
    db.commit()

@router.delete("/delete-items/{item_id}") # Project delete
async def delete_items(user: user_dependency, db: db_dependency, item_id:int):
    item = db.query(Project).filter(Project.id == item_id).filter(Project.user_id == user.get('id')).first()

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.delete(item)
        db.commit()



@router.get("/get-items") # Project get/query
async def get_items(user:user_dependency, db: db_dependency): # fotoğraflar static/uploads içerisinde bulunuyor
    return db.query(Project).filter(Project.user_id == user.get('id'))

