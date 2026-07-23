# myapp/routers/items.py
# -----------------------------------------------------------
# All /items routes live here as a separate APIRouter.
# -----------------------------------------------------------

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    id: int
    name: str
    price: float


ITEMS = [Item(id=1, name="Pen", price=50), Item(id=2, name="Book", price=300)]


@router.get("/")
def list_items():
    return ITEMS


@router.get("/{item_id}")
def get_item(item_id: int):
    item = next((i for i in ITEMS if i.id == item_id), None)
    if not item:
        raise HTTPException(404, detail=f"Item {item_id} not found")
    return item
