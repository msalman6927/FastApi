# myapp/routers/users.py
# -----------------------------------------------------------
# All /users routes live here as an APIRouter (a "mini-app").
# -----------------------------------------------------------

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# prefix -> every route below is under /users; tags -> grouped in /docs.
router = APIRouter(prefix="/users", tags=["users"])


class User(BaseModel):
    id: int
    name: str


USERS = [User(id=1, name="Ayesha"), User(id=2, name="Bilal")]


@router.get("/")                 # -> GET /users/
def list_users():
    return USERS


@router.get("/{user_id}")        # -> GET /users/{user_id}
def get_user(user_id: int):
    user = next((u for u in USERS if u.id == user_id), None)
    if not user:
        raise HTTPException(404, detail=f"User {user_id} not found")
    return user
