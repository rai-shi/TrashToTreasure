from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from utils.models import Base
from utils.database import engine, SessionLocal #SessionLocal'i kullanarak aslında veritabanıyla bağlantı sağlıyoruz
from routers.auth import router as auth_router
from routers.project import router as project_router
from routers.user import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)