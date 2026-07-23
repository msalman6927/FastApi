# solutions.py  (Day 21 - reference)
# -----------------------------------------------------------
# The assignment asks for a MULTI-FILE package (blogapp/). For a runnable
# single-file reference, this shows the same MECHANICS (APIRouter + Settings)
# in one file. In your submission, split these into the folder structure:
#
#   blogapp/__init__.py
#   blogapp/config.py        -> the Settings class below
#   blogapp/main.py          -> the app + include_router calls below
#   blogapp/routers/posts.py -> the posts_router below
#   blogapp/routers/comments.py -> the comments_router below
#   blogapp/dependencies.py  -> the pagination dependency below
#
# SETUP: pip install "fastapi[standard]" pydantic-settings
# RUN:   fastapi dev solutions.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# ===== config.py =====
class Settings(BaseSettings):
    app_name: str = "Blog API"
    admin_email: str = "admin@example.com"
    debug: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()


# ===== dependencies.py =====
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# ===== routers/posts.py =====
posts_router = APIRouter(prefix="/posts", tags=["posts"])

class Post(BaseModel):
    id: int
    title: str

POSTS = [Post(id=1, title="Hello"), Post(id=2, title="World")]

@posts_router.get("/")
def list_posts(page: dict = Depends(pagination)):
    return POSTS[page["skip"]: page["skip"] + page["limit"]]

@posts_router.get("/{post_id}")
def get_post(post_id: int):
    post = next((p for p in POSTS if p.id == post_id), None)
    if not post:
        raise HTTPException(404, detail=f"Post {post_id} not found")
    return post

@posts_router.post("/", status_code=201)
def create_post(post: Post):
    POSTS.append(post)
    return post


# ===== routers/comments.py =====
comments_router = APIRouter(prefix="/comments", tags=["comments"])
COMMENTS: list[str] = []

@comments_router.get("/")
def list_comments(page: dict = Depends(pagination)):
    return COMMENTS[page["skip"]: page["skip"] + page["limit"]]

@comments_router.post("/", status_code=201)
def add_comment(text: str):
    COMMENTS.append(text)
    return {"comments": COMMENTS}


# ===== main.py =====
app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(posts_router)
app.include_router(comments_router)

@app.get("/")
def root():
    return {"app": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
