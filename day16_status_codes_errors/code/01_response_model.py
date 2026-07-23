# 01_response_model.py
# -----------------------------------------------------------
# GOAL: Control what the API RETURNS with response_model. Hide secrets
# (like passwords) by using separate input and output models.
#
# RUN:  fastapi dev 01_response_model.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel   # (using str for email to avoid the extra pydantic[email] install)

app = FastAPI()


# What the client SENDS (includes a password).
class UserIn(BaseModel):
    name: str
    email: str
    password: str


# What the API RETURNS (NO password - it must never leave the server).
class UserOut(BaseModel):
    name: str
    email: str


USERS: list[UserIn] = []


# response_model=UserOut -> FastAPI filters the returned object down to
# only UserOut's fields. Even though we return a UserIn (with password),
# the response contains ONLY name + email.
@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    USERS.append(user)
    return user            # password is stripped from the response automatically


# For lists, use response_model=list[UserOut].
@app.get("/users", response_model=list[UserOut])
def list_users():
    return USERS           # each item filtered to UserOut


# Try in /docs: POST a user with a password, then look at the response and
# GET /users - the password is nowhere in the output. That's response_model.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
