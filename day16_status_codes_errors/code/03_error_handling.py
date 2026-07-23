# 03_error_handling.py
# -----------------------------------------------------------
# GOAL: Fail GRACEFULLY with HTTPException instead of crashing (500) or
# returning wrong data. This is how an API says "404 Not Found" properly.
#
#   return               -> success path
#   raise HTTPException  -> controlled failure path (correct status + JSON)
#
# RUN:  fastapi dev 03_error_handling.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


DB: dict[int, Item] = {1: Item(name="Pen", price=50)}


# 404 NOT FOUND when the resource doesn't exist.
@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = DB.get(item_id)
    if item is None:
        # raise (not return!) stops the function and sends a proper error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


# 409 CONFLICT when trying to create something that already exists.
@app.post("/items/{item_id}", status_code=status.HTTP_201_CREATED)
def create_item(item_id: int, item: Item):
    if item_id in DB:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item {item_id} already exists",
        )
    DB[item_id] = item
    return item


# 400 BAD REQUEST for a semantically invalid request (beyond type validation).
@app.post("/discount")
def apply_discount(price: float, percent: float):
    if percent > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Discount percent cannot exceed 100",
        )
    return {"final_price": price * (1 - percent / 100)}


# Try in /docs:
#   GET /items/1   -> 200 (exists)
#   GET /items/99  -> 404 with {"detail": "Item 99 not found"}
#   POST /items/1  -> 409 (already exists)
#   POST /discount?price=100&percent=150 -> 400
#
# WRONG WAY (do not do this): returning {"error": "not found"} with status 200.
# The STATUS CODE must reflect the failure so clients/agents understand it.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
