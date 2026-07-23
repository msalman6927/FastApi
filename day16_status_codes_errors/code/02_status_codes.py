# 02_status_codes.py
# -----------------------------------------------------------
# GOAL: Return the CORRECT HTTP status code per operation (Day 11 conventions).
#   POST create -> 201 Created
#   DELETE      -> 204 No Content (empty body)
#   GET/PUT     -> 200 OK (default)
#
# RUN:  fastapi dev 02_status_codes.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, status      # `status` gives readable named constants
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


DB: dict[int, Item] = {}
_next_id = 1


# 201 CREATED: use the named constant (clearer than the number 201).
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    global _next_id
    DB[_next_id] = item
    result = {"id": _next_id, "item": item}
    _next_id += 1
    return result


# 200 OK (default) for reads.
@app.get("/items")
def list_items():
    return DB


# 204 NO CONTENT: a successful delete returns NO body. Do not return anything.
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    DB.pop(item_id, None)
    # returning None -> empty 204 response


# In /docs, notice each endpoint documents its status code. Watch the actual
# codes: POST -> 201, DELETE -> 204, GET -> 200.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
