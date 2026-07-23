# 05_practical_items_api.py
# -----------------------------------------------------------
# GOAL: A realistic read API combining everything today:
#   - path parameter to fetch one item
#   - query parameters for search + pagination
#   - an Enum to restrict the "sort" value (shows as a dropdown in /docs)
#   - correct route ORDER (static before dynamic)
#
# RUN:  fastapi dev 05_practical_items_api.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from enum import Enum
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI(title="Products API", version="1.0.0")


class Product(BaseModel):
    id: int
    name: str
    price: float


PRODUCTS = [
    Product(id=1, name="Pen", price=50),
    Product(id=2, name="Notebook", price=120),
    Product(id=3, name="Backpack", price=800),
    Product(id=4, name="Water Bottle", price=300),
    Product(id=5, name="Pencil Box", price=150),
]


# Restrict sort to only these values (422 for anything else; dropdown in docs).
class SortBy(str, Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    name = "name"


# ---- STATIC routes FIRST (before the dynamic /products/{id}) ----
@app.get("/products", summary="List/search/sort products")
def list_products(
    q: str | None = Query(default=None, description="Search in product name"),
    sort: SortBy = SortBy.name,
    limit: int = Query(default=10, ge=1, le=50),
    skip: int = Query(default=0, ge=0),
):
    results = PRODUCTS

    # Search (query param)
    if q:
        results = [p for p in results if q.lower() in p.name.lower()]

    # Sort (Enum query param)
    if sort == SortBy.price_asc:
        results = sorted(results, key=lambda p: p.price)
    elif sort == SortBy.price_desc:
        results = sorted(results, key=lambda p: p.price, reverse=True)
    else:  # SortBy.name
        results = sorted(results, key=lambda p: p.name)

    # Pagination (query params)
    return {"count": len(results), "items": results[skip: skip + limit]}


# ---- DYNAMIC route AFTER the static ones ----
@app.get("/products/{product_id}", summary="Get one product by id")
def get_product(product_id: int = Path(gt=0)):
    for p in PRODUCTS:
        if p.id == product_id:
            return p
    # Proper 404 error handling comes on Day 16; for now a simple message.
    return {"error": f"product {product_id} not found"}


# Try in /docs:
#   /products                              -> all, sorted by name
#   /products?q=pen                        -> search "pen"
#   /products?sort=price_desc&limit=3      -> top 3 by price desc
#   /products/2                            -> one product
#   /products/999                          -> not found message

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
