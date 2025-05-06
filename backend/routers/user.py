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
from utils.auth import *



router = APIRouter(
    prefix="/user",
    tags=["User"]
)

current_directory = os.path.dirname(os.path.abspath(__file__)) # get current directory, routers
backend_directory = os.path.dirname(current_directory) # backend directory
project_directory = os.path.dirname(backend_directory) # project directory
templates_directory = os.path.join(project_directory, "frontend", "templates") # templates directory

templates = Jinja2Templates(directory=templates_directory)


user_dependency = Annotated[dict, Depends(verify_token)]
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/profile",
            status_code=status.HTTP_200_OK)
async def get_user_profile(request: Request,
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
    print("get_user_profile")
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]
    print(token)
    verified_user = verify_token(token)
    if verified_user is None:
        return redirect_to_login()
    
    user = get_user_by_id(db=db, user_id=verified_user["user_id"])
    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User not found"})
    user_content = {
            "user":{
                    "id":user.id,
                    "username":user.username,
                    "email":user.email,
                    "first_name":user.first_name,
                    "last_name":user.last_name
                    }
                }       
    return JSONResponse(content=user_content)




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
        
