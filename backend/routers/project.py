"""
get_recyclable_item_image
get_materials
create_ideas
get_roadmap
"""
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv
import os

import google.generativeai as genai
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