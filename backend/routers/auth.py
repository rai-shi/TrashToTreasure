"""
endpoints:

    register
    login
    logout
"""

from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from backend.utils.database import SessionLocal, get_db
from backend.utils.models import User, Base
from backend.utils.auth import *


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

current_directory = os.path.dirname(os.path.abspath(__file__)) # get current directory, routers
backend_directory = os.path.dirname(current_directory) # backend directory
project_directory = os.path.dirname(backend_directory) # project directory
templates_directory = os.path.join(project_directory, "frontend", "templates") # templates directory

templates = Jinja2Templates(directory=templates_directory)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_token)]


@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", 
                                      {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", 
                                      {"request": request})


@router.post("/register", status_code=status.HTTP_201_CREATED)  
async def create_user(createUserRequest: CreateUserRequest,
                      db: db_dependency):
    """
    Create a new user

    input
    - username: str
    - email: str
    - first_name: str
    - last_name: str
    - password: str

    return
    - id: int
    - username: str
    - email: str
    - first_name: str
    - last_name: str

    """
    # kullanıcı var mı kontrolü
    existing_user = db.query(User).filter(User.email == createUserRequest.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(
        username = createUserRequest.username,
        email = createUserRequest.email,
        first_name = createUserRequest.first_name,
        last_name = createUserRequest.last_name,
        hashed_password = bcrypt_context.hash(createUserRequest.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(
        content={"user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }},
        status_code=status.HTTP_201_CREATED
    )


@router.post("/login", 
             status_code=status.HTTP_200_OK,
             response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                      db: db_dependency):
    """
    Login user

    input
    - username: str
    - password: str

    return 
    - access token
    - token type
    """
    
    user = authenticate_user(db, 
                             form_data.username, 
                             form_data.password)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                             detail="Invalid credentials")
    
    token = create_access_token(
        username=user.username, 
        user_id=user.id, 
        expire_time=timedelta(minutes=30)
    )

    # return {
    #     "access_token": token,
    #     "token_type": "bearer",
    # }
    return JSONResponse(
        content={
                    "access_token": token,
                    "token_type": "bearer",
                },
        status_code=status.HTTP_201_CREATED
    )



@router.post("/logout")
async def logout_user(request: Request):
    """
    Logout user
    - return 
        - redirect to login page
    """
    redirect_response = RedirectResponse(url="/auth/login-page", 
                                         status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie("access_token")
    return redirect_response
    
