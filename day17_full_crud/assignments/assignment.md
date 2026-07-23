# Day 17 Assignment — Full CRUD API

**Module 02 · Day 17**
**Goal:** Build a complete CRUD API for one resource, using the three-model pattern, correct status codes, and 404 handling.

---

## Task 1 (Core) — Contacts CRUD
Build a `Contact` API (in-memory) with:
- Models: `ContactCreate` (`name`, `phone`, `email`), `ContactOut` (adds `id`).
- `POST /contacts` → 201, returns created contact.
- `GET /contacts` → list all.
- `GET /contacts/{id}` → one or 404.
- `PUT /contacts/{id}` → replace or 404.
- `DELETE /contacts/{id}` → 204 or 404.
Use a `get_or_404` helper.

---

## Task 2 (Medium) — Add PATCH
1. Add a `ContactUpdate` model with all fields optional.
2. `PATCH /contacts/{id}` updates only provided fields (use `model_dump(exclude_unset=True)`).
3. Test: PATCH only the phone; confirm name/email are unchanged.

---

## Task 3 (Medium) — Search + count
1. `GET /contacts/search?q=...` returns contacts whose name contains `q` (case-insensitive). (Place it before `/contacts/{id}` — route order!)
2. `GET /contacts/stats` returns `{"total": N}`.

---

## Task 4 (Challenge) — Prevent duplicates + client script
1. `POST /contacts` returns **409** if a contact with the same `phone` already exists.
2. Write a `client.py` (using `requests`) that creates 2 contacts, lists them, patches one, deletes one, and prints each response — proving the whole API works.

---

## Submission
`contacts_api.py` (+ `client.py`) → repo `batch5-day17` with a README.

## Checklist
- [ ] All 5 CRUD routes with correct status codes
- [ ] 404 on missing id for get/put/patch/delete
- [ ] PATCH updates only provided fields
- [ ] Search route ordered before the dynamic `/{id}` route
- [ ] 409 on duplicate phone
- [ ] Client script exercises every endpoint
