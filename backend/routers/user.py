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
        auth_header = request.headers.get("Authorization")
        # Token'ı çıkar
        token = auth_header.split(" ")[1]

        verified_user = verify_token(token)
        print(verified_user)
        if verified_user is None:
            return redirect_to_login()
        
        user = get_user_by_id(db=db, user_id=verified_user["user_id"])
        return {"user": {
                            "id":user.id,
                            "username":user.username,
                            "email":user.email,
                            "first_name":user.first_name,
                            "last_name":user.last_name
        }}
    except:
        return redirect_to_login()

        



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
        




@router.get("/my-projects",
            status_code=status.HTTP_200_OK)
async def get_user_projects(request: Request,
                             user_: user_dependency,
                             db: db_dependency):
    """
    Get user projects
    - return 
        - projects
            - id
            - name
            - description
            - image
            - created_at
            
    """
    # check token 
    # get user projects by user id
    # return them
    return JSONResponse(content="deneme")



@router.get("/my-projects/{project_id}",
            status_code=status.HTTP_200_OK)
async def get_user_project( request: Request,
                            user_: user_dependency ,
                            db: db_dependency ,
                            project_id: int = Path(gt=0),
                            ):
    # check token 
    # get user project by user id and project id
    # return it
    example = {
        "id": 1,
        "name": "Project 1",
        "description": "Project 1 short description",
        "roadmap": "Project 1 roadmap",
        "image": "path/to/image.jpg",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return JSONResponse(content=example)