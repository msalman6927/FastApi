# 02_multiple_routes.py
# -----------------------------------------------------------
# GOAL: Several routes in one app. Learn that:
#   - the URL comes from the DECORATOR path, not the function name
#   - each route can respond to a specific HTTP method
#
# RUN:  fastapi dev 02_multiple_routes.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI

app = FastAPI()


# The path is "/", the function name (home) is just a Python name.
@app.get("/")
def home():
    return {"page": "home"}


# The URL is "/about" because of the decorator - NOT because of the
# function name. You could name the function anything.
@app.get("/about")
def some_random_name():
    return {"page": "about", "course": "Agentic AI - Batch 5"}


@app.get("/contact")
def contact():
    return {"email": "info@a2skills.example", "phone": "+92-300-0000000"}


# Two routes can SHARE a path with DIFFERENT methods (RESTful design).
# GET /items  -> read the list
@app.get("/items")
def list_items():
    return {"action": "read", "items": ["pen", "book", "bag"]}


# POST /items -> pretend to create (we handle real request bodies on Day 15)
@app.post("/items")
def create_item():
    return {"action": "create", "message": "an item would be created here"}


# TIP: after running, EDIT one of these return values, SAVE, and refresh the
# browser - `fastapi dev` auto-reloads so you see changes instantly.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
