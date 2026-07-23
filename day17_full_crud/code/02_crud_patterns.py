# 02_crud_patterns.py
# -----------------------------------------------------------
# GOAL: The professional THREE-MODEL pattern + PATCH (partial update).
#   Create (no id) | Update (all optional) | Out (with id)
#
# RUN:  fastapi dev 02_crud_patterns.py  ->  /docs
# -----------------------------------------------------------

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Products CRUD (3-model pattern)")


class ProductBase(BaseModel):        # shared fields
    name: str
    price: float
    in_stock: bool = True


class ProductCreate(ProductBase):    # CREATE input (no id)
    pass


class ProductUpdate(BaseModel):      # PATCH input: EVERYTHING optional
    name: str | None = None
    price: float | None = None
    in_stock: bool | None = None


class ProductOut(ProductBase):       # RESPONSE (adds id)
    id: int


DB: dict[int, ProductOut] = {}
_next = 1


def get_or_404(pid: int) -> ProductOut:
    p = DB.get(pid)
    if p is None:
        raise HTTPException(404, detail=f"Product {pid} not found")
    return p


@app.post("/products", response_model=ProductOut, status_code=201)
def create(p: ProductCreate):
    global _next
    out = ProductOut(id=_next, **p.model_dump())
    DB[_next] = out
    _next += 1
    return out


@app.get("/products", response_model=list[ProductOut])
def list_all():
    return list(DB.values())


# PATCH = PARTIAL update. Only the fields the client SENT are changed.
@app.patch("/products/{pid}", response_model=ProductOut)
def patch(pid: int, changes: ProductUpdate):
    current = get_or_404(pid)
    # exclude_unset=True -> only fields the client actually provided
    updates = changes.model_dump(exclude_unset=True)
    updated = current.model_copy(update=updates)   # apply just those fields
    DB[pid] = updated
    return updated


# Compare in /docs:
#   PUT would require ALL fields (full replace).
#   PATCH /products/1 with body {"price": 99} changes ONLY the price;
#   name and in_stock stay as they were. That's the power of exclude_unset.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
