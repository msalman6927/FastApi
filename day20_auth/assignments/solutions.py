# solutions.py  (Day 20 - API key + JWT auth, hashed passwords, per-user data)
# SETUP: pip install "fastapi[standard]" pyjwt "passlib[bcrypt]"
# RUN:   fastapi dev solutions.py  ->  /docs

import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI(title="Day 20 Solutions")

# Task 4: read secret from env (fallback for dev); on Day 21 this moves to .env
SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
ALGO = "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# ===== Task 1 - API key =====
@app.get("/public")
def public():
    return {"open": True}

def require_key(x_api_key: str = Header(...)):
    if x_api_key != "secret123":
        raise HTTPException(401, "Invalid API key")

@app.get("/private", dependencies=[Depends(require_key)])
def private():
    return {"secret": "with a valid key you can see this"}


# ===== Task 2 - hashing (WHY: hashing is one-way; if the DB leaks, the
# original passwords are NOT recoverable. Never store plaintext.) =====
@app.get("/hash-demo")
def hash_demo():
    h = pwd.hash("mypassword")
    return {"hash": h, "verify_ok": pwd.verify("mypassword", h)}


# ===== Tasks 3-4 - JWT login + per-user tasks =====
USERS: dict[str, str] = {}          # username -> hashed password
TASKS: dict[str, list[str]] = {}    # username -> tasks


class RegisterIn(BaseModel):
    username: str
    password: str


def create_token(username: str) -> str:
    return jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
        SECRET, algorithm=ALGO)


def current_user(token: str = Depends(oauth2)) -> str:
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGO])["sub"]
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired token")


@app.post("/register", status_code=201)
def register(data: RegisterIn):
    if data.username in USERS:
        raise HTTPException(409, "Username taken")
    USERS[data.username] = pwd.hash(data.password)
    TASKS[data.username] = []
    return {"registered": data.username}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    hashed = USERS.get(form.username)
    if not hashed or not pwd.verify(form.password, hashed):
        raise HTTPException(401, "Incorrect username or password")
    return {"access_token": create_token(form.username), "token_type": "bearer"}


@app.get("/me")
def me(user: str = Depends(current_user)):
    return {"you_are": user}


@app.get("/tasks")
def my_tasks(user: str = Depends(current_user)):
    return {"user": user, "tasks": TASKS.get(user, [])}


@app.post("/tasks", status_code=201)
def add_task(text: str, user: str = Depends(current_user)):
    TASKS.setdefault(user, []).append(text)
    return {"tasks": TASKS[user]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
