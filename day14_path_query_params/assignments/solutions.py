# solutions.py  (Instructor solution reference for Day 14 assignment)
# -----------------------------------------------------------
# Path & query parameters, validation with Path()/Query(), Enums,
# and correct route ordering (static before dynamic).
#
# SETUP:  pip install "fastapi[standard]"
# RUN:    fastapi dev solutions.py   ->  http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from enum import Enum
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI(title="Day 14 Solutions")


# ===========================================================
# TASK 1 — Path parameter
# ===========================================================
BOOKS = {1: "1984", 2: "Sapiens", 3: "Dune"}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"id": book_id, "title": BOOKS.get(book_id, "unknown")}


# ===========================================================
# TASK 2 — Pagination with query params
# ===========================================================
NUMBERS = list(range(1, 31))          # 1..30


@app.get("/items")
def list_items(limit: int = 5, skip: int = 0):
    return {"limit": limit, "skip": skip, "items": NUMBERS[skip: skip + limit]}


# ===========================================================
# TASK 3 — Search + required/optional + ROUTE ORDER
# ===========================================================
MOVIES = ["The Matrix", "Inception", "The Dark Knight",
          "Interstellar", "The Prestige", "Dunkirk"]

# STATIC routes FIRST so they aren't swallowed by /movies/{movie_id}.
@app.get("/movies/popular")
def popular_movies():
    # If this were AFTER /movies/{movie_id}, "popular" would try to become
    # an int, fail, and 422 - never reaching here. Order matters!
    return {"popular": MOVIES[:3]}


@app.get("/movies/search")
def search_movies(q: str):            # required query param (no default)
    return {"query": q, "results": [m for m in MOVIES if q.lower() in m.lower()]}


# DYNAMIC route AFTER the static ones.
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int = Path(ge=0, lt=len(MOVIES))):
    return {"id": movie_id, "title": MOVIES[movie_id]}


# ===========================================================
# TASK 4 — Products API with validation + Enum
# ===========================================================
class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str


PRODUCTS = [
    Product(id=1, name="Pen", price=50, category="stationery"),
    Product(id=2, name="Notebook", price=120, category="stationery"),
    Product(id=3, name="Backpack", price=800, category="bags"),
    Product(id=4, name="Water Bottle", price=300, category="accessories"),
    Product(id=5, name="Pencil Box", price=150, category="stationery"),
]


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


# STATIC before DYNAMIC.
@app.get("/products")
def list_products(
    category: str | None = None,
    max_price: float | None = Query(default=None, gt=0),
    sort: SortOrder = SortOrder.asc,
    limit: int = Query(default=10, ge=1, le=50),
):
    results = PRODUCTS
    if category:
        results = [p for p in results if p.category == category]
    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    results = sorted(results, key=lambda p: p.price,
                     reverse=(sort == SortOrder.desc))
    return {"count": len(results[:limit]), "items": results[:limit]}


@app.get("/products/{product_id}")
def get_product(product_id: int = Path(gt=0)):
    for p in PRODUCTS:
        if p.id == product_id:
            return p
    return {"error": f"product {product_id} not found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
