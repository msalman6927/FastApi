# 04_validation.py
# -----------------------------------------------------------
# GOAL: Add CONSTRAINTS and docs to parameters with Path() and Query().
# Same idea as Pydantic's Field() from Day 12, applied to URL inputs.
# Invalid input -> automatic 422 response.
#
# RUN:  fastapi dev 04_validation.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(
    # PATH validation: item_id must be a positive integer (> 0).
    item_id: int = Path(gt=0, description="Positive item id"),
    # QUERY validation: q is optional, but if given must be 3-50 chars.
    q: str | None = Query(default=None, min_length=3, max_length=50),
    # QUERY validation: limit defaults to 10 and must be between 1 and 100.
    limit: int = Query(default=10, ge=1, le=100),
):
    return {"item_id": item_id, "q": q, "limit": limit}


# Try these in /docs or the browser:
#   /items/5                    -> ok
#   /items/0                    -> 422 (item_id must be > 0)
#   /items/-3                   -> 422
#   /items/5?q=ab               -> 422 (q too short, min_length=3)
#   /items/5?limit=500          -> 422 (limit must be <= 100)
#   /items/5?q=phone&limit=20   -> ok


# A REQUIRED query param WITH constraints: use Query(...) (the literal ...)
# or simply give no default. Here 'keyword' is required and must be >= 2 chars.
@app.get("/search")
def search(keyword: str = Query(min_length=2, description="What to search for")):
    return {"keyword": keyword}
# /search              -> 422 (keyword required)
# /search?keyword=a    -> 422 (too short)
# /search?keyword=api  -> ok


# The constraints above are also DISPLAYED in /docs automatically, and the
# "Try it out" form will show the min/max rules. Validation + documentation
# from the same declarations - that's the FastAPI payoff.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
