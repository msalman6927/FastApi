# Day 18 Assignment — Databases (SQLModel + SQLite)

**Module 02 · Day 18**
**Goal:** Persist a resource in a real SQLite database with full CRUD, using a session dependency, and confirm data survives restarts.

> `pip install sqlmodel "fastapi[standard]"`. Run with `fastapi dev your_file.py`.

---

## Task 1 (Core) — Books table + create/read
1. Define a table model `Book` (`id` PK, `title`, `author`, `year`).
2. Set up the engine (`sqlite:///books.db`) and create tables at startup.
3. `POST /books` — persist a book, return it with its new id.
4. `GET /books` — return all books.
5. Restart the server and confirm previously created books are still there.

---

## Task 2 (Medium) — Read one, update, delete
1. `GET /books/{id}` → the book or 404.
2. `PATCH /books/{id}` → update provided fields or 404.
3. `DELETE /books/{id}` → 204 or 404.
Use `session.get`, `session.delete`, `commit`, `refresh`.

---

## Task 3 (Medium) — Input/output models
1. Add `BookCreate` (no id) as the POST body and `BookPublic` (with id) as the response (`response_model`).
2. Keep the `Book` table model separate from these API models.

---

## Task 4 (Challenge) — Query features
1. `GET /books?author=...` → filter by author (use `select(Book).where(Book.author == author)`).
2. `GET /books?min_year=...` → books from that year onward.
3. Combine filters when both query params are provided.

---

## Submission
`books_db.py` → repo `batch5-day18` with a README (include `pip install sqlmodel`).

## Checklist
- [ ] Data persists across restarts (real DB file)
- [ ] Full CRUD with 404 handling
- [ ] Session provided via `Depends(get_session)`
- [ ] Separate `Create`/`Public` API models vs the table model
- [ ] Query filtering with `select().where()`
