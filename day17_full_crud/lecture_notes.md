# Day 17 — Full CRUD API (In-Memory)

**Module:** 02 — FastAPI | **Duration:** 2 hours
**Prerequisite:** Days 13–16 (routes, params, bodies, response_model, status, errors)

> Where we are: You've learned every piece separately. Today you assemble them into a **complete CRUD API** — Create, Read (all + one), Update, Delete — for a single resource, done the professional way. This is the standard shape of virtually every web backend. Master this pattern and you can build the data layer of any app. Storage is still in-memory today; a real database arrives tomorrow (Day 18).

---

# PART 1 — INSTRUCTOR DEEP-DIVE

## 1.1 CRUD = the four operations, mapped to HTTP

| Operation | HTTP | Route | Success code |
|-----------|------|-------|--------------|
| **Create** | POST | `/items` | 201 |
| **Read all** | GET | `/items` | 200 |
| **Read one** | GET | `/items/{id}` | 200 (or 404) |
| **Update** | PUT/PATCH | `/items/{id}` | 200 (or 404) |
| **Delete** | DELETE | `/items/{id}` | 204 (or 404) |

This table *is* a REST resource. Every backend you'll ever build repeats this pattern for each resource (users, products, orders…). It's muscle memory worth drilling.

## 1.2 The three-model pattern (professional structure)

Real CRUD APIs use **separate models for different jobs** — an application of OOP inheritance (Day 6) and the input/output split (Day 16):
```python
class ItemBase(BaseModel):        # shared fields
    name: str
    price: float

class ItemCreate(ItemBase):       # what the client sends to CREATE (no id yet)
    pass

class ItemUpdate(BaseModel):      # PATCH: all fields OPTIONAL (partial update)
    name: str | None = None
    price: float | None = None

class ItemOut(ItemBase):          # what the API RETURNS (includes server-assigned id)
    id: int
```
Why: the client shouldn't send the `id` (the server assigns it); a partial update needs all-optional fields; the response needs the `id`. Separate models keep each concern clean and the `/docs` accurate.

## 1.3 PUT vs PATCH (finally, side by side)
- **PUT** = replace the **whole** resource. Client sends all fields. Missing fields get overwritten/reset.
- **PATCH** = update **some** fields. Client sends only what changes; the rest stay.

PATCH implementation uses `model_dump(exclude_unset=True)` to grab only the fields the client actually provided:
```python
@app.patch("/items/{item_id}", response_model=ItemOut)
def patch_item(item_id: int, changes: ItemUpdate):
    item = DB.get(item_id) or not_found(item_id)
    updates = changes.model_dump(exclude_unset=True)   # only provided fields
    updated = item.model_copy(update=updates)          # apply them
    DB[item_id] = updated
    return updated
```
`exclude_unset=True` is the key: it distinguishes "field not sent" from "field sent as null." That's what makes PATCH truly partial.

## 1.4 A reusable "not found" helper
Repeating the 404 raise is noisy. Factor it:
```python
def get_or_404(item_id: int) -> Item:
    item = DB.get(item_id)
    if item is None:
        raise HTTPException(404, detail=f"Item {item_id} not found")
    return item
```
Now every read/update/delete calls `get_or_404(id)` — DRY (OOP module value). This is a taste of the "dependencies" we formalize on Day 19.

## 1.5 Auto-incrementing ids & storage
In-memory storage is a `dict[int, Item]` plus a counter for new ids. This mirrors a database table (id → row) closely enough that swapping to a real DB tomorrow is a small change. Keep the storage logic in one place so the swap is easy.

## 1.6 Common mistakes
1. Letting the client set the `id` on create (id is the server's job).
2. PATCH that overwrites unset fields with `None` (use `exclude_unset=True`).
3. Forgetting 404 on update/delete of a missing id.
4. Inconsistent response shapes across endpoints (use `response_model` everywhere).
5. Duplicating the 404 logic instead of a helper.
6. Returning the deleted object on a 204 (204 = no body).

## 1.7 Tricky questions
- **"PUT or PATCH by default?"** PUT for full replacement, PATCH for partial edits. Many APIs offer both; PATCH is friendlier for clients.
- **"Where do ids come from?"** The server assigns them (counter now, DB auto-increment tomorrow). Clients never invent ids on create.
- **"Is in-memory data lost on restart?"** Yes — it lives in RAM. That's exactly why we add a database on Day 18.

---

# PART 2 — 2-HOUR LECTURE PLAN

| Time | Segment | Action |
|------|---------|--------|
| 0–10 | Recap + the CRUD table | Show the 5-route table; "today we build all of it." |
| 10–40 | Build C/R/R (live) | `code/01_crud_items.py`: POST(201), GET all, GET one(404). |
| 40–70 | Update + Delete (live) | Add PUT, DELETE(204); the `get_or_404` helper. |
| 70–95 | Three-model pattern + PATCH | `code/02_crud_patterns.py`: In/Out/Update, PATCH with `exclude_unset`. |
| 95–108 | Client test + assignment | Run `code/03_client.py` to exercise every endpoint; brief assignment. |
| 108–120 | Q&A / buffer | Preview Day 18 (databases: persist across restarts). |

**Tip:** build `01` incrementally, testing each route in `/docs` as you add it. The "restart the server → data is gone" moment (end) is the perfect setup for tomorrow's database lesson.

---

# PART 3 — CODE FILES (`code/`)
1. `01_crud_items.py` — complete CRUD in one file with a `get_or_404` helper.
2. `02_crud_patterns.py` — the three-model pattern + PATCH partial update.
3. `03_client.py` — a `requests` client that creates, reads, updates, and deletes.

**Run server:** `fastapi dev 01_crud_items.py` → `/docs`. **Run client:** in a 2nd terminal, `python 03_client.py` (server must be running).

---

# PART 4 — STUDENT HANDOUT (recap)
- **CRUD → HTTP:** POST /items (201), GET /items (200), GET /items/{id} (200/404), PUT/PATCH /items/{id} (200/404), DELETE /items/{id} (204/404).
- **Three-model pattern:** `Create` (no id), `Update` (all optional), `Out` (with id). Keeps input/output clean and safe.
- **PATCH** uses `model_dump(exclude_unset=True)` to update only provided fields.
- **`get_or_404` helper** removes repeated 404 code (DRY).
- In-memory data vanishes on restart → tomorrow we add a database.
- Homework: full CRUD for a resource of your choice. Push to `batch5-day17`.
- **Next (Day 18):** databases — persist data with SQLite + SQLAlchemy so it survives restarts.
