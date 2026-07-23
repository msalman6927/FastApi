# 02_query_parameters.py
# -----------------------------------------------------------
# GOAL: Query parameters are the ?key=value parts of a URL. Any function
# parameter NOT in the path is a query parameter.
#   - has a default  -> OPTIONAL query parameter
#   - no default     -> REQUIRED query parameter
#
# RUN:  fastapi dev 02_query_parameters.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI

app = FastAPI()

ITEMS = [f"item_{i}" for i in range(1, 21)]     # item_1 .. item_20


# limit and skip are QUERY params (not in the path). Both have defaults,
# so both are OPTIONAL. This is classic pagination.
@app.get("/items")
def list_items(limit: int = 10, skip: int = 0):
    # /items                 -> limit=10, skip=0
    # /items?limit=5         -> limit=5,  skip=0
    # /items?limit=5&skip=15 -> limit=5,  skip=15
    page = ITEMS[skip: skip + limit]
    return {"limit": limit, "skip": skip, "items": page}


# A REQUIRED query parameter: no default -> must be provided.
@app.get("/search")
def search(q: str, limit: int = 10):
    # /search           -> 422 (q is required!)
    # /search?q=book    -> matches items containing "book"
    matches = [i for i in ITEMS if q in i]
    return {"query": q, "limit": limit, "results": matches[:limit]}


# An OPTIONAL + NULLABLE query parameter: q may be omitted entirely.
@app.get("/filter")
def filter_items(q: str | None = None):
    if q is None:
        return {"note": "no filter applied", "items": ITEMS}
    return {"filter": q, "items": [i for i in ITEMS if q in i]}


# NOTE: query parameter ORDER in the URL does not matter:
#   /items?limit=5&skip=2  ==  /items?skip=2&limit=5

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
