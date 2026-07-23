# 01_crud_items.py
# -----------------------------------------------------------
# GOAL: A COMPLETE CRUD API for one resource (items), in memory.
#   Create (POST 201), Read all (GET), Read one (GET/404),
#   Update (PUT/404), Delete (DELETE 204/404).
#
# RUN:  fastapi dev 01_crud_items.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Items CRUD API")


class ItemIn(BaseModel):          # client sends this (no id)
    name: str
    price: float


class ItemOut(ItemIn):            # API returns this (adds id) - inheritance (OOP Day 6)
    id: int


DB: dict[int, ItemOut] = {}
_next_id = 1


# Reusable 404 helper (DRY) - a preview of "dependencies" (Day 19).
def get_or_404(item_id: int) -> ItemOut:
    item = DB.get(item_id)
    if item is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Item {item_id} not found")
    return item


# CREATE
@app.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemIn):
    global _next_id
    created = ItemOut(id=_next_id, **item.model_dump())
    DB[_next_id] = created
    _next_id += 1
    return created


# READ ALL
@app.get("/items", response_model=list[ItemOut])
def list_items():
    return list(DB.values())


# READ ONE
@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    return get_or_404(item_id)


# UPDATE (full replace)
@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemIn):
    get_or_404(item_id)                          # 404 if missing
    updated = ItemOut(id=item_id, **item.model_dump())
    DB[item_id] = updated
    return updated


# DELETE
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    get_or_404(item_id)                          # 404 if missing
    del DB[item_id]
    # 204 -> no body


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
