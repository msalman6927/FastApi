# taskmanager/main.py  -- the entry point ties everything together
#
# SETUP: pip install "fastapi[standard]" sqlmodel pyjwt "passlib[bcrypt]" pydantic-settings
# RUN (from the code/ folder, after copying .env.example to .env):
#     fastapi dev taskmanager/main.py
#   or:
#     uvicorn taskmanager.main:app --reload
# Open http://127.0.0.1:8000/docs

from fastapi import FastAPI

from .config import settings
from .database import create_db_and_tables
from .routers import auth_routes, tasks

app = FastAPI(title=settings.app_name)

app.include_router(auth_routes.router)
app.include_router(tasks.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"app": settings.app_name, "docs": "/docs"}

# FULL FLOW to test in /docs:
#   1) POST /register  {username, password}
#   2) Click "Authorize" (username + password -> calls /login)
#   3) POST /tasks, GET /tasks -> only YOUR tasks
#   4) Register a second user -> they cannot see the first user's tasks
