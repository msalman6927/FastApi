# 03_secure_api.py
# -----------------------------------------------------------
# GOAL: Tie it together - register + login + a protected per-user resource.
# Users register (password hashed), log in (get JWT), and manage THEIR notes.
#
# SETUP:  pip install "fastapi[standard]" pyjwt "passlib[bcrypt]"
# RUN:    fastapi dev 03_secure_api.py  ->  /docs
# -----------------------------------------------------------

from datetime import datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI(title="Secure Notes API")

SECRET, ALGO = "CHANGE-ME-secret", "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

USERS: dict[str, str] = {}          # username -> hashed password
NOTES: dict[str, list[str]] = {}    # username -> their notes


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
    USERS[data.username] = pwd.hash(data.password)   # store the HASH
    NOTES[data.username] = []
    return {"registered": data.username}


@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    hashed = USERS.get(form.username)
    if not hashed or not pwd.verify(form.password, hashed):
        raise HTTPException(401, "Incorrect username or password")
    return {"access_token": create_token(form.username), "token_type": "bearer"}


# Each user sees/creates only THEIR OWN notes (authorization by identity).
@app.get("/notes")
def my_notes(user: str = Depends(current_user)):
    return {"user": user, "notes": NOTES.get(user, [])}


@app.post("/notes", status_code=201)
def add_note(text: str, user: str = Depends(current_user)):
    NOTES.setdefault(user, []).append(text)
    return {"user": user, "notes": NOTES[user]}


# FLOW to test in /docs:
#   1) POST /register {username, password}
#   2) "Authorize" with those credentials (calls /login for you)
#   3) POST /notes?text=... and GET /notes -> only your notes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
