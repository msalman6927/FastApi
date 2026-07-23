# 02_dependencies.py
# -----------------------------------------------------------
# GOAL: Dependencies with Depends() - write shared logic ONCE, inject it
# into many routes. This is dependency injection (OOP Day 9) built into FastAPI.
#
# RUN:  fastapi dev 02_dependencies.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, Depends

app = FastAPI()

ITEMS = [f"item_{i}" for i in range(1, 51)]
USERS = [f"user_{i}" for i in range(1, 51)]


# A DEPENDENCY: a function whose return value FastAPI injects into routes.
# It reads skip/limit from the query string (FastAPI wires that up for us).
def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


# Both routes REUSE the same pagination logic - no duplication (DRY).
@app.get("/items")
def list_items(page: dict = Depends(pagination)):
    return ITEMS[page["skip"]: page["skip"] + page["limit"]]


@app.get("/users")
def list_users(page: dict = Depends(pagination)):
    return USERS[page["skip"]: page["skip"] + page["limit"]]


# ---- SUB-DEPENDENCIES: a dependency can depend on ANOTHER dependency ----
def query_or_default(q: str | None = None):
    return q or "everything"


def search_context(q: str = Depends(query_or_default),
                   page: dict = Depends(pagination)):
    # This dependency composes two other dependencies.
    return {"searching_for": q, **page}


@app.get("/search")
def search(ctx: dict = Depends(search_context)):
    return ctx


# Try in /docs:
#   /items?skip=5&limit=3   -> reuses pagination
#   /users?limit=2          -> same dependency, different route
#   /search?q=book&limit=5  -> composed dependencies

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
