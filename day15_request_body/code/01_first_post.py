# 01_first_post.py
# -----------------------------------------------------------
# GOAL: Accept a JSON request body by declaring a Pydantic model as a
# function parameter. THE model IS the body.
#
# RUN:   fastapi dev 01_first_post.py
# TEST:  open http://127.0.0.1:8000/docs -> POST /users -> "Try it out"
#        (a JSON editor appears; edit and click Execute)
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# This model describes the SHAPE of the JSON body we expect (Day 12).
class User(BaseModel):
    name: str
    age: int
    email: str


# Because 'user' is typed as a Pydantic model, FastAPI reads it from the
# REQUEST BODY (not the URL), validates it, and passes a clean User object.
@app.post("/users")
def create_user(user: User):
    # 'user' is a fully validated User object - use it like any object.
    return {
        "message": f"User {user.name} created!",
        "age_next_year": user.age + 1,
        "data": user,            # returning the model -> JSON automatically
    }


# Compare: this is a QUERY parameter (simple type), NOT a body.
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# THE RULE:
#   parameter typed as a Pydantic model  -> request BODY
#   simple type (int/str/...) not in path -> QUERY parameter
#   name in the path {} -> PATH parameter

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
