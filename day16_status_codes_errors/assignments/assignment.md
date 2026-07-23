# Day 16 Assignment — Response Models, Status Codes & Errors

**Module 02 · Day 16**
**Goal:** Shape responses with `response_model`, return correct status codes, and handle errors with `HTTPException`.

> Run with `fastapi dev your_file.py`, test in `/docs`.

---

## Task 1 (Easy) — Hide a field with response_model
1. Define `AccountIn` (`username`, `email`, `password`) and `AccountOut` (`username`, `email`).
2. `POST /accounts` accepts `AccountIn`, uses `response_model=AccountOut`, stores it, returns it.
3. Confirm the response has **no** password.

---

## Task 2 (Medium) — Correct status codes
1. Keep an in-memory `dict` of products.
2. `POST /products` → status **201**, returns the created product (with its id).
3. `DELETE /products/{id}` → status **204**, empty body.
4. `GET /products` → 200, list all.

---

## Task 3 (Medium) — 404 handling
1. `GET /products/{id}` → return the product, or `raise HTTPException(404)` with a helpful detail if missing.
2. `PUT /products/{id}` → update if it exists, else 404.
3. Test both missing and existing ids in `/docs`.

**Expected `GET /products/999`:**
```json
{"detail": "Product 999 not found"}   // with HTTP status 404
```

---

## Task 4 (Challenge) — A clean mini-API
Build a `Book` API with `BookIn`/`BookOut` (hide an internal `secret_notes` field), in-memory storage, and:
- `POST /books` (201, response_model=BookOut)
- `GET /books` (200, response_model=list[BookOut])
- `GET /books/{id}` (200 or 404)
- `PUT /books/{id}` (200 or 404)
- `DELETE /books/{id}` (204 or 404)
- `POST /books` should return **409** if a book with the same `title` already exists.

---

## Submission
`api_day16.py` → repo `batch5-day16` with a README. 

## Checklist
- [ ] `response_model` hides secret fields
- [ ] 201 on create, 204 on delete, 200 on read/update
- [ ] `HTTPException` used for 404 (and 409)
- [ ] Never returns an error dict with a 200 status
