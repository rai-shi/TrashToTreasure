"""
endpoints:

    register
    login
    logout
    profile
    get_user_projects
"""

from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
#from utils.database import SessionLocal
#from utils.models import User
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/users",
    tags=["Authentication"]
)