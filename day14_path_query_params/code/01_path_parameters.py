# 01_path_parameters.py
# -----------------------------------------------------------
# GOAL: Path parameters make routes DYNAMIC. A {piece} of the URL becomes
# a function argument, auto-converted and validated by its type hint.
#
# RUN:  fastapi dev 01_path_parameters.py
#       then open http://127.0.0.1:8000/docs
# TRY:  /users/5   (works)     /users/abc  (422 - not an int)
# -----------------------------------------------------------

from fastapi import FastAPI

app = FastAPI()

# In-memory "database".
USERS = {1: "Ayesha", 2: "Bilal", 3: "Chetan"}


# {user_id} in the path becomes the function argument user_id.
# The name inside {} MUST match the parameter name.
@app.get("/users/{user_id}")
def get_user(user_id: int):        # ": int" -> FastAPI converts "5" -> 5
    # If the id doesn't exist we just report it (proper 404 comes on Day 16).
    name = USERS.get(user_id, "unknown")
    return {"user_id": user_id, "name": name}


# Another example: a string path parameter (no conversion needed).
@app.get("/greet/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}


# ==========================================================================
# THE ROUTE-ORDER GOTCHA (very important!)
# --------------------------------------------------------------------------
# FastAPI matches routes TOP-TO-BOTTOM and uses the FIRST that fits.
# A fixed route defined AFTER a matching dynamic route is UNREACHABLE.
#
# CORRECT ORDER: put the SPECIFIC/fixed route BEFORE the dynamic one.
# ==========================================================================

# Specific route FIRST...
@app.get("/products/featured")
def featured_product():
    return {"product": "Featured item of the week!"}


# ...dynamic route AFTER. (If these two were swapped, "/products/featured"
# would try to become an int, fail, and return 422 - never reaching the
# featured route.)
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"product_id": product_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
