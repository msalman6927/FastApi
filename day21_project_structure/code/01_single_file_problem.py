# 01_single_file_problem.py
# -----------------------------------------------------------
# GOAL: Show the "everything in one file" anti-pattern. Imagine this with
# 40 routes, 15 models, DB code, config, and auth all crammed together -
# unreadable and unmaintainable. Then we refactor into the myapp/ package.
#
# RUN:  fastapi dev 01_single_file_problem.py
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# --- users stuff ---
class User(BaseModel):
    id: int
    name: str

USERS = [User(id=1, name="Ayesha"), User(id=2, name="Bilal")]

@app.get("/users")
def list_users():
    return USERS

@app.get("/users/{uid}")
def get_user(uid: int):
    return next((u for u in USERS if u.id == uid), {"error": "not found"})

# --- items stuff (different concern, same file...) ---
class Item(BaseModel):
    id: int
    name: str

ITEMS = [Item(id=1, name="Pen"), Item(id=2, name="Book")]

@app.get("/items")
def list_items():
    return ITEMS

@app.get("/items/{iid}")
def get_item(iid: int):
    return next((i for i in ITEMS if i.id == iid), {"error": "not found"})

# Now imagine adding orders, auth, payments, config, database... all HERE.
# It becomes a nightmare. The fix: split by responsibility into a package.
# See the myapp/ folder for the clean version.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
