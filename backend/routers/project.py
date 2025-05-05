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
import google.generativeai as genai
import os
import uuid
import aiofiles
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import markdown
from bs4 import BeautifulSoup


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)

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