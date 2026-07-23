# 05_practical_notes_api.py
# -----------------------------------------------------------
# GOAL: A small practical API that RECEIVES bodies: create and list notes,
# plus a NESTED-body example (an order with a list of items).
# (Full CRUD + real DB come on Days 17-18.)
#
# RUN:  fastapi dev 05_practical_notes_api.py  ->  /docs
#
# BONUS: a Python client using `requests` is at the bottom - run it in a
# SECOND terminal (while the server runs) with:  python 05_practical_notes_api.py client
# -----------------------------------------------------------

import sys
from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API", version="1.0.0")


# ---- Simple body ----
class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str


class Note(NoteIn):          # inherits title+content, adds an id (OOP Day 6!)
    id: int


NOTES: list[Note] = []
_next_id = 1


@app.post("/notes", status_code=status.HTTP_201_CREATED, summary="Create a note")
def create_note(note: NoteIn):
    global _next_id
    saved = Note(id=_next_id, **note.model_dump())   # build a Note from the input
    NOTES.append(saved)
    _next_id += 1
    return saved


@app.get("/notes", summary="List all notes")
def list_notes():
    return NOTES


# ---- Nested body: an order containing a list of items (Day 12 nesting) ----
class OrderItem(BaseModel):
    name: str
    qty: int = Field(gt=0)


class Order(BaseModel):
    customer: str
    items: list[OrderItem]       # a LIST of nested models


@app.post("/orders", summary="Create an order (nested body)")
def create_order(order: Order):
    total_qty = sum(i.qty for i in order.items)
    return {
        "customer": order.customer,
        "line_items": len(order.items),
        "total_quantity": total_qty,
    }


# ---- Optional Python client to demonstrate calling the API from code ----
def run_client():
    import requests
    base = "http://127.0.0.1:8000"
    print("Creating a note...")
    r = requests.post(f"{base}/notes", json={"title": "Day 15", "content": "POST bodies!"})
    print("  status:", r.status_code, "| created:", r.json())

    print("Creating an order (nested body)...")
    order = {"customer": "Ayesha", "items": [
        {"name": "Pen", "qty": 3}, {"name": "Book", "qty": 1}]}
    r = requests.post(f"{base}/orders", json=order)
    print("  status:", r.status_code, "| result:", r.json())

    print("Listing notes...")
    print("  ", requests.get(f"{base}/notes").json())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        run_client()             # `python 05_practical_notes_api.py client`
    else:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
