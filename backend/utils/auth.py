from datetime import timedelta, datetime, timezone
from pathlib import Path

from fastapi import Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from utils.models import User
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv

current_directory = os.path.dirname(os.path.abspath(__file__)) # utils directory, routers
backend_directory = os.path.dirname(current_directory) # backend directory

environment_path = backend_directory + "/.env"

load_dotenv(environment_path)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=11, max_length=50)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(db: Session, 
                      username: str, 
                      password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail="Invalid credentials")
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail="Invalid credentials")
    return user


def create_access_token(username:str, user_id:int, expire_time:timedelta):
    payload = {"sub": username, 
                 "user_id": user_id, 
                 "exp": datetime.now(tz=timezone.utc) + expire_time}
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Invalid token")
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", 
                                         status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("access_token")
    return redirect_response


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user
