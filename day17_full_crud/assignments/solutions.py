# solutions.py  (Day 17 - full CRUD, contacts)
# SETUP: pip install "fastapi[standard]"
# RUN:   fastapi dev solutions.py  ->  /docs

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Contacts CRUD")


class ContactCreate(BaseModel):
    name: str
    phone: str
    email: str

class ContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None

class ContactOut(ContactCreate):
    id: int


DB: dict[int, ContactOut] = {}
_next = 1


def get_or_404(cid: int) -> ContactOut:
    c = DB.get(cid)
    if c is None:
        raise HTTPException(404, detail=f"Contact {cid} not found")
    return c


@app.post("/contacts", response_model=ContactOut, status_code=201)
def create(c: ContactCreate):
    global _next
    # Task 4: 409 on duplicate phone
    if any(x.phone == c.phone for x in DB.values()):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            detail=f"Phone {c.phone} already exists")
    out = ContactOut(id=_next, **c.model_dump())
    DB[_next] = out
    _next += 1
    return out


@app.get("/contacts", response_model=list[ContactOut])
def list_all():
    return list(DB.values())


# Task 3: STATIC routes BEFORE the dynamic /{id} route
@app.get("/contacts/search", response_model=list[ContactOut])
def search(q: str):
    return [c for c in DB.values() if q.lower() in c.name.lower()]


@app.get("/contacts/stats")
def stats():
    return {"total": len(DB)}


@app.get("/contacts/{cid}", response_model=ContactOut)
def get_one(cid: int):
    return get_or_404(cid)


@app.put("/contacts/{cid}", response_model=ContactOut)
def replace(cid: int, c: ContactCreate):
    get_or_404(cid)
    out = ContactOut(id=cid, **c.model_dump())
    DB[cid] = out
    return out


@app.patch("/contacts/{cid}", response_model=ContactOut)
def patch(cid: int, changes: ContactUpdate):
    current = get_or_404(cid)
    updated = current.model_copy(update=changes.model_dump(exclude_unset=True))
    DB[cid] = updated
    return updated


@app.delete("/contacts/{cid}", status_code=status.HTTP_204_NO_CONTENT)
def delete(cid: int):
    get_or_404(cid)
    del DB[cid]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
