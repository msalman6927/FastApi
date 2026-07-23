# Day 16 — Response Models, Status Codes & Error Handling

**Module:** 02 — FastAPI | **Duration:** 2 hours
**Prerequisite:** Days 13–15 (routes, params, request bodies), Day 12 (Pydantic), Day 11 (status codes)

> Where we are: Your API can read and receive data. But it always returns 200 and exposes *everything*. Real APIs **control what they return** (hide passwords, shape output), **set correct status codes** (201 on create, 204 on delete), and **fail gracefully** (404 when a resource is missing) instead of crashing. Today you learn `response_model`, `status_code`, and `HTTPException` — the three tools that make an API professional. This directly answers yesterday's open question: "what if the id doesn't exist?"

---

# PART 1 — INSTRUCTOR DEEP-DIVE

## 1.1 `response_model` — controlling the output shape

By default FastAPI serializes whatever you return. That's risky: if your `User` object has a `password`, returning it leaks the password. `response_model` declares the **exact shape of the response**, and FastAPI filters the output to match it.

```python
class UserIn(BaseModel):     # what the client SENDS (includes password)
    name: str
    email: str
    password: str

class UserOut(BaseModel):    # what the API RETURNS (no password!)
    name: str
    email: str

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    save(user)
    return user              # FastAPI strips it down to UserOut -> password hidden
```

Key points:
- **Input model vs output model** is a core professional pattern: `UserIn` (with password) for the request body, `UserOut` (without) for the response. Even though we `return user` (a `UserIn`), FastAPI only emits the `UserOut` fields.
- `response_model` also **validates and documents** the response — the `/docs` "Responses" section shows the exact output schema.
- Use `response_model=list[UserOut]` for endpoints returning lists.
- Extra fields in the returned object are silently dropped; missing required fields raise a server error (good — catches bugs).
- Handy option: `response_model_exclude_none=True` drops `None` fields from the output.

This is the encapsulation principle (OOP Day 5) applied to APIs: expose only what should be public.

## 1.2 Status codes — saying the right thing

Default success is 200. But REST conventions (Day 11) expect specific codes:
- **201 Created** after a successful POST.
- **204 No Content** after a DELETE (no body returned).
- **200 OK** for GET/PUT/PATCH.

Set the default per route with `status_code`:
```python
from fastapi import status   # named constants, clearer than raw numbers

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create(item: Item): ...

@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int): ...      # return nothing
```
`status.HTTP_201_CREATED` reads better than `201` and prevents typos. For **dynamic** status (e.g., 200 if updated, 201 if created), inject the `Response` object and set `response.status_code` — mention lightly.

## 1.3 `HTTPException` — failing gracefully

When something's wrong (resource missing, not allowed), you must return a proper error status, not crash with a 500. Raise `HTTPException`:
```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = DB.get(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item
```
- `raise HTTPException(...)` immediately stops the function and sends an error response with your status + a JSON `{"detail": ...}`.
- Common uses: **404** (not found), **400** (bad request), **401/403** (auth — Day 20), **409** (conflict, e.g. duplicate).
- The `detail` can be a string or any JSON-able object.
- You can add custom headers via `headers=...`.

Mental model: **`return` = success path; `raise HTTPException` = controlled failure path.** Both produce clean JSON responses; only the status differs.

## 1.4 Why not just let it crash?

If you don't handle a missing item, either you return `null`/wrong data (confusing) or an unhandled exception becomes a **500 Internal Server Error** (looks like *your* bug, leaks stack traces). `HTTPException` turns "the client asked for something that isn't there" into an honest **404** — a *client* problem (4xx), clearly communicated. Correct status codes are how clients (and other programs, and AI agents) know what happened without reading your mind.

## 1.5 Common mistakes
1. Returning a model with secrets and forgetting `response_model` → data leak.
2. Using 200 for everything → clients can't distinguish create/delete/update.
3. Returning an error dict with status 200 (`{"error": "not found"}` + 200) → wrong; the *status code* must reflect failure. Use `HTTPException`.
4. `return HTTPException(...)` instead of `raise` → does nothing useful; you must **raise** it.
5. 204 route that returns a body → 204 means *no content*; return nothing.
6. Catching your own `HTTPException` accidentally in a broad `try/except` → let it propagate.

## 1.6 Tricky questions & answers
- **"Why two models (In/Out)?"** Different concerns: input may include a password or fields the server sets; output should hide/omit them. Separate models keep each clean and safe.
- **"`response_model` vs just returning a model?"** `response_model` *enforces and documents* the output shape and filters extra fields — a guarantee, not just a return value.
- **"When 400 vs 404 vs 422?"** 422 = body/params failed validation (FastAPI auto). 404 = resource doesn't exist. 400 = a valid-shaped request that's still wrong for another reason.
- **"Can I customize the error JSON?"** Yes — `detail` can be structured, and you can add global exception handlers (advanced; mention).

---

# PART 2 — 2-HOUR LECTURE PLAN

| Time | Segment | Action |
|------|---------|--------|
| 0–10 | Recap + hook | Day 15 recap; "what if the id doesn't exist?" Show a route returning a password (the leak). |
| 10–35 | `response_model` (live) | `code/01_response_model.py`: `UserIn`/`UserOut`, hide password, list response. |
| 35–60 | Status codes (live) | `code/02_status_codes.py`: 201 on create, 204 on delete, `status.*` constants. |
| 60–90 | `HTTPException` (live) | `code/03_error_handling.py`: 404 on missing, 400/409 examples; return vs raise. |
| 90–108 | Practical + assignment | Combine into a mini items API with proper codes/errors; brief assignment. |
| 108–120 | Q&A / buffer | Test 404s in `/docs`; preview Day 17 (full CRUD). |

**Tip:** the password-leak demo (0–35) sells `response_model` instantly. The 404 demo (60–90) is the emotional payoff — an API that fails *correctly*.

---

# PART 3 — CODE FILES (`code/`, run in order)
1. `01_response_model.py` — input vs output models; hide fields; list responses.
2. `02_status_codes.py` — 201/204/200 with `status.*`.
3. `03_error_handling.py` — `HTTPException` for 404/400/409; return vs raise.

**Run:** `fastapi dev 01_response_model.py` → `http://127.0.0.1:8000/docs`.

---

# PART 4 — STUDENT HANDOUT (recap)
- **`response_model=Model`** shapes/filters the output — use separate `In`/`Out` models to hide secrets like passwords.
- **`status_code=status.HTTP_201_CREATED`** (etc.) sets the right code; 201 create, 204 delete, 200 read/update.
- **`raise HTTPException(status_code=404, detail=...)`** for controlled failures — never return an error dict with a 200.
- `return` = success; `raise HTTPException` = failure. Both emit clean JSON.
- Homework: build an items API with `response_model`, correct status codes, and a 404 on missing items. Push to `batch5-day16`.
- **Next (Day 17):** put it all together into a full **CRUD** API (Create/Read/Update/Delete) in one resource.
