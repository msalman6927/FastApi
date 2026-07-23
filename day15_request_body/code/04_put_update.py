# 04_put_update.py
# -----------------------------------------------------------
# GOAL: PUT to UPDATE/REPLACE a resource. PUT usually takes BOTH:
#   - a PATH parameter (WHICH resource) and
#   - a BODY (the new data).
#
# RUN:  fastapi dev 04_put_update.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


# A small in-memory "database": id -> Item
DB: dict[int, Item] = {
    1: Item(name="Pen", price=50),
    2: Item(name="Notebook", price=120),
}


@app.get("/items")
def list_items():
    return DB


# POST = CREATE. Server appends with a new id (not idempotent).
@app.post("/items", status_code=201)
def create_item(item: Item):
    new_id = max(DB.keys(), default=0) + 1
    DB[new_id] = item
    return {"id": new_id, "item": item}


# PUT = UPDATE/REPLACE the item at {item_id} with the body (idempotent).
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    # (Proper 404 for a missing id comes on Day 16; today we just overwrite.)
    DB[item_id] = item
    return {"id": item_id, "updated": item}


# Try in /docs:
#   POST /items   body {"name":"Bag","price":800}   -> creates id 3
#   PUT  /items/1 body {"name":"Blue Pen","price":60} -> replaces item 1
#   GET  /items   -> see the changes
#
# POST vs PUT:
#   POST /items    -> create a NEW item (id assigned by server)
#   PUT  /items/1  -> replace the EXISTING item 1 (you say which id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
