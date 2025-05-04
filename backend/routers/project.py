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
#from utils.models import Base, Project
#from utils.database import engine, SessionLocal #SessionLocal'i kullanarak aslında veritabanıyla bağlantı sağlıyoruz
from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import google.generativeai as genai
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import markdown
from bs4 import BeautifulSoup


router = APIRouter(
    prefix="/project",
    tags=["Project"]
)