"""
endpoints:
    register
    login
    refresh
"""

from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
<<<<<<< HEAD
from json import JSONDecodeError

=======
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
from utils.database import SessionLocal, get_db
from utils.models import User, Base
from utils.auth import *


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(verify_token)]

@router.post("/register", status_code=status.HTTP_201_CREATED)  
async def create_user(request: Request, db: db_dependency):
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
    try:
        print("Register endpoint çağrıldı")
        # JSON request body'sini al
        data = await request.json()
        print(f"Alınan veri: {data}")
        username = data.get("username")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        
        # Validation
        if not all([username, email, first_name, last_name, password]):
            print(f"Eksik veri: username={username}, email={email}, first_name={first_name}, last_name={last_name}, password={'*' * len(password) if password else None}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All fields are required"
            )
            
        # Kullanıcı var mı kontrolü
        existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
            print(f"Kullanıcı zaten var: {email}")
        raise HTTPException(status_code=400, detail="User already exists")
    
        # Şifreyi hashle
        print("Şifre hashlenecek")
        hashed_password = get_password_hash(password)
        print("Şifre hashlendi")
        
        try:
            user = User(
                username = username,
                email = email,
                first_name = first_name,
                last_name = last_name,
                hashed_password = hashed_password,
    )
            print("Kullanıcı oluşturuldu, veritabanına eklenecek")
    db.add(user)
    db.commit()
            print("Veritabanı commit yapıldı")
    db.refresh(user)
            print(f"Kullanıcı başarıyla oluşturuldu: ID={user.id}")

<<<<<<< HEAD
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        except Exception as e:
            print(f"Veritabanı hatası: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    except JSONDecodeError as e:
        print(f"JSON parse hatası: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON"
        )
    except Exception as e:
        print(f"Beklenmeyen hata: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
=======
    return JSONResponse(
        content={"user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }},
        status_code=status.HTTP_201_CREATED
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
    )


@router.post("/login", 
             status_code=status.HTTP_200_OK)
async def login_user(request: Request, db: db_dependency):
    """
    Login user

    input
    - username: str
    - password: str

    return 
    - access token
    - token type
    """
    try:
        # JSON request body'sini al
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username and password are required"
            )
    
        user = authenticate_user(db, username, password)
    if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid credentials"
            )
    
    token = create_access_token(
        username=user.username, 
        user_id=user.id, 
        expire_time=timedelta(minutes=30)
    )

<<<<<<< HEAD
    return {
        "access_token": token,
        "token_type": "bearer",
            "user_id": user.id
        }
    except JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
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
        # Get user from database to ensure they still exist
        db_user = get_user_by_id(db, user["user_id"])
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists"
            )
        
        # Create new token
        new_token = create_access_token(
            username=db_user.username,
            user_id=db_user.id,
            expire_time=timedelta(minutes=30)
        )
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
=======
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
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
    


@router.get("/profile",
            status_code=status.HTTP_200_OK)
async def get_user_profile(request: Request,
                            user_: user_dependency,
                            db: db_dependency):
    """
    Get user profile
    - return 
        - user
            - id
            - username
            - email
            - first_name
            - last_name
    """
    try:
        # token = request.cookies.get("access_token")

        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        print(verified_user)
        if verified_user is None:
            return redirect_to_login()
        
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
        user_content = {
                            "id":user.id,
                            "username":user.username,
                            "email":user.email,
                            "first_name":user.first_name,
                            "last_name":user.last_name
        }       
        return JSONResponse(content=user_content)
    except:
        return redirect_to_login()

