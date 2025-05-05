<<<<<<< HEAD
"""
endpoints:
    profile
    get_user_projects
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from typing import Annotated, List
from sqlalchemy.orm import Session

from utils.database import get_db
from utils.models import User, Project
=======
from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, Path, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from jose import jwt, JWTError

from pydantic import BaseModel, Field
from passlib.context import CryptContext
from typing import Annotated

from sqlalchemy.orm import Session

from utils.database import SessionLocal, get_db
from utils.models import User, Base
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
from utils.auth import *



router = APIRouter(
    prefix="/user",
    tags=["User"]
)

user_dependency = Annotated[dict, Depends(verify_token)]
db_dependency = Annotated[Session, Depends(get_db)]

<<<<<<< HEAD
class UserProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    image: str

@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_user_profile(user: user_dependency, db: db_dependency):
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
        # Extract user_id from token payload
        if not user or "user_id" not in user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token - missing user_id"
            )
        
        user_id = user["user_id"]
        
        # Get user from database
        try:
            user_data = get_user_by_id(db=db, user_id=user_id)
        except HTTPException as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id {user_id} not found"
                )
            raise e
        
        # Return user profile data
        return {
            "user": {
                "id": user_data.id,
                "username": user_data.username,
                "email": user_data.email,
                "first_name": user_data.first_name,
                "last_name": user_data.last_name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/projects", status_code=status.HTTP_200_OK, response_model=List[UserProjectResponse])
async def get_user_projects(user: user_dependency, db: db_dependency):
    """
    Get user projects
    - return
        - projects list
    """
    try:
        user_id = user["user_id"]
        
        # Gerçek uygulamada veritabanından kullanıcının projeleri çekilecek
        # Şimdilik örnek veriler döndürüyoruz
        
        return [
            {
                "id": 1,
                "name": "Cam Şişe Lamba",
                "description": "Eski şişelerden dekoratif bir lamba projesi",
                "image": "https://via.placeholder.com/300x200?text=Sise+Lamba"
            },
            {
                "id": 2,
                "name": "Ahşap Kitaplık",
                "description": "Eski ahşap parçalardan kitaplık projesi",
                "image": "https://via.placeholder.com/300x200?text=Ahsap+Kitaplik"
            }
        ]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
=======


# @router.get("/profile",
#             status_code=status.HTTP_200_OK)
# async def get_user_profile(request: Request,
#                             user_: user_dependency,
#                             db: db_dependency):
#     """
#     Get user profile
#     - return 
#         - user
#             - id
#             - username
#             - email
#             - first_name
#             - last_name
#     """
#     try:
#         token = request.cookies.get("access_token")
#         verified_user = await verify_token(token)
#         if verified_user is None:
#             return redirect_to_login()
        
#         user = get_user_by_id(db=db, user_id=verified_user["user_id"])
#         print(user.username)
#         user_dict = {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "first_name": user.first_name,
#             "last_name": user.last_name
#         }
#         return templates.TemplateResponse("profile.html", 
#                                           {
#                                             "request": request,
#                                             "user": user_dict,    
#                                             }
#                                           )
#     except:
#         return redirect_to_login()
        
>>>>>>> 0afa934b42d025cb26f46261f4ee5b91dd0733b9
