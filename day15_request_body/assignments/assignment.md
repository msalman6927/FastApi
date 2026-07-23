# Day 15 Assignment — Request Body (POST/PUT)

**Module 02 · Day 15**
**Goal:** Accept JSON request bodies using Pydantic models, validate them, store them in memory, and combine body + path + query.

> Reminder: activate your `.venv`. Run with `fastapi dev your_file.py`, test in `/docs` → "Try it out". A Pydantic-model parameter = the request body.

---

## Task 1 (Easy) — First POST
1. Define a Pydantic model `Student` with `name: str`, `age: int`, `email: str`.
2. Add `POST /students` that accepts a `Student` body and returns `{"message": "created <name>", "student": <the student>}`.
3. Test in `/docs` with a valid body. Then send `age` as `"twenty"` and observe the **422**.

**Expected (valid body):**
```json
{"message": "created Ayesha", "student": {"name": "Ayesha", "age": 25, "email": "a@mail.com"}}
```

---

## Task 2 (Medium) — Validation + store + list
1. Define a model `Product` with:
   - `name: str` (min_length 2),
   - `price: float` (> 0),
   - `in_stock: bool = True`.
2. Keep an in-memory list `PRODUCTS`.
3. `POST /products` — validate, append, return the created product with status **201**.
4. `GET /products` — return all products.
5. Show that `price: -10` returns a 422 and is NOT added.

**Expected:** after two valid POSTs, `GET /products` returns a list of 2 products; a POST with `price:-10` returns 422.

---

## Task 3 (Medium) — Body + path + query, and PUT
1. Keep an in-memory dict `TASKS: dict[int, Task]` where `Task` has `title: str` and `done: bool = False`. Pre-populate with 2 tasks.
2. `POST /tasks` — create a new task (server assigns the next id), return id + task, status 201.
3. `PUT /tasks/{task_id}` — replace the task at that id with the body; also accept a query param `notify: bool = False`; return the id, updated task, and whether to notify.
4. `GET /tasks` — list all.

**Expected at `PUT /tasks/1?notify=true` with body `{"title":"Updated","done":true}`:**
```json
{"id": 1, "updated": {"title": "Updated", "done": true}, "notify": true}
```

---

## Task 4 (Challenge) — Nested body: a shopping cart
1. Define:
   - `CartItem`: `product: str`, `quantity: int` (> 0), `price: float` (> 0).
   - `Cart`: `customer: str`, `items: list[CartItem]`.
2. `POST /carts` — accept a `Cart`, compute and return:
   - `customer`,
   - `item_count` (number of line items),
   - `total_quantity` (sum of quantities),
   - `total_price` (sum of `quantity * price`).
3. Test with a cart of 3 items in `/docs`. Then send an item with `quantity: 0` and observe the nested 422 (note the error path, e.g. `("body","items",1,"quantity")`).

**Expected (valid cart, example):**
```json
{"customer": "Ayesha", "item_count": 3, "total_quantity": 6, "total_price": 1150.0}
```

---

## Submission
Put your app in `body_api.py`, commit to repo `batch5-day15`, push to GitHub, and submit the link. Add a `README.md` with run instructions and example request bodies to paste into `/docs`.

## Grading checklist
- [ ] POST endpoints accept a Pydantic-model body
- [ ] Invalid bodies return 422 and are not stored
- [ ] POST returns status 201 and the created object
- [ ] Task 3 combines path + body + query in one PUT endpoint
- [ ] Task 4 uses a nested model (list of items) and computes totals
- [ ] Repo has a `README.md` with example bodies
