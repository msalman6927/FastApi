# 02_jwt_auth.py
# -----------------------------------------------------------
# GOAL: Real user login with JWT.
#   - hash passwords (NEVER store plaintext)
#   - POST /login verifies credentials and issues a signed token
#   - get_current_user dependency verifies the token on protected routes
#
# SETUP:  pip install "fastapi[standard]" pyjwt "passlib[bcrypt]"
# RUN:    fastapi dev 02_jwt_auth.py  ->  /docs  ->  "Authorize"
# -----------------------------------------------------------

from datetime import datetime, timedelta, timezone
import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

app = FastAPI(title="JWT Auth Demo")

# --- config (in real apps these go in .env - Day 21) ---
SECRET = "CHANGE-ME-to-a-long-random-secret"
ALGO = "HS256"
TOKEN_MINUTES = 30

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="login")   # extracts "Bearer <token>"

# A fake user "database": username -> hashed password.
# We hash "wonderland" so no plaintext password is stored.
FAKE_USERS = {
    "ayesha": {"username": "ayesha", "hashed_password": pwd.hash("wonderland")}
}


# ---- helpers ----
def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)


def get_current_user(token: str = Depends(oauth2)) -> str:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload["sub"]                     # the username
    except jwt.PyJWTError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token")


# ---- LOGIN: verify credentials, return a token ----
# OAuth2PasswordRequestForm reads form fields "username" and "password".
@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = FAKE_USERS.get(form.username)
    # Compare the submitted password against the stored HASH (never plaintext).
    if not user or not pwd.verify(form.password, user["hashed_password"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    return {"access_token": create_token(user["username"]), "token_type": "bearer"}


# ---- PROTECTED routes ----
@app.get("/me")
def read_me(user: str = Depends(get_current_user)):
    return {"you_are": user}


@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"secret": "42", "for_user": user}


# HOW TO TEST in /docs:
#   1) Click "Authorize", enter username=ayesha password=wonderland, submit.
#   2) Now /me and /protected work (200). Without it -> 401.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
