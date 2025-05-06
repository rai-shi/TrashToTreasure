from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from utils.database import SessionLocal, get_db
from utils.models import User, Base
from utils.auth import *


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

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# @router.get("/login-page")
# def render_login_page(request: Request):
#     return templates.TemplateResponse("login.html", 
#                                       {"request": request})


# @router.get("/register-page")
# def render_register_page(request: Request):
#     return templates.TemplateResponse("register.html", 
#                                       {"request": request})


@router.post("/register", status_code=status.HTTP_201_CREATED)  
async def create_user(
                        createUserRequest: CreateUserRequest,
                      db: db_dependency):

    # kullanıcı var mı kontrolü
    existing_user = db.query(User).filter(User.email == createUserRequest.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    try:
    
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    return JSONResponse(
        # user yerine direkt göndermek gerekebilir
        content={"user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }},
        status_code=status.HTTP_201_CREATED
    )


@router.post("/login", status_code=status.HTTP_200_OK) # response_model=Token)
async def login_user(request: LoginRequest, db: db_dependency):
    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required"
        )
    user = authenticate_user(db, username, password)
    token = create_access_token(
        username=user.username, 
        user_id=user.id, 
        expire_time=timedelta(minutes=30)
    )
    return JSONResponse(
        content={
                    "access_token": token,
                    "token_type": "bearer",
                    "user_id": user.id
                },
        status_code=status.HTTP_200_OK
    )


@router.post("/refresh")
async def refresh_token(user: user_dependency, db: db_dependency):
    """
    Refresh access token
    
    input:
    - Authorization header with current token
    
    return:
    - new access token
    """
    try:
        db_user = get_user_by_id(db, user["user_id"])

        new_token = create_access_token(
            username=db_user.username,
            user_id=db_user.id,
            expire_time=timedelta(minutes=30)
        )
        return JSONResponse(content={
                                "access_token": new_token,
                                "token_type": "bearer",
                                "user_id": user.id
                            },
                            status_code=status.HTTP_201_CREATED
                        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ! cookies olduğu sürece çalışabilir
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
    

