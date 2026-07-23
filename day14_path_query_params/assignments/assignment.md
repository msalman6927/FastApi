# Day 14 Assignment — Path & Query Parameters

**Module 02 · Day 14**
**Goal:** Make your API dynamic with path parameters (to identify resources) and query parameters (to filter, search, paginate), with validation.

> Reminder: activate your `.venv`. Run with `fastapi dev your_file.py`, test in `/docs`. Remember: **static routes before dynamic routes**, and a query param with a default is optional / without one is required.

---

## Task 1 (Easy) — Path parameter
1. Create an app with an in-memory dict of books: `{1: "1984", 2: "Sapiens", 3: "Dune"}`.
2. Add `GET /books/{book_id}` that returns `{"id": ..., "title": ...}` for the given id (`book_id: int`).
3. Test `/books/2` (works) and `/books/abc` (should return **422**). Note what the 422 says.

**Expected at `/books/2`:**
```json
{"id": 2, "title": "Sapiens"}
```

---

## Task 2 (Medium) — Query parameters for pagination
1. Create a list of 30 numbers (or fake items).
2. Add `GET /items` with query params `limit: int = 5` and `skip: int = 0`.
3. Return the correct "page" of items plus the `limit` and `skip` used.
4. Test `/items`, `/items?limit=10`, and `/items?limit=3&skip=6`.

**Expected at `/items?limit=3&skip=6` (example):**
```json
{"limit": 3, "skip": 6, "items": [7, 8, 9]}
```

---

## Task 3 (Medium) — Search + required vs optional + the order gotcha
1. Add a list of movies (at least 6, as strings).
2. Add `GET /movies/popular` returning a fixed list of 3 "popular" movies.
3. Add `GET /movies/{movie_id}` returning the movie at that index/id.
4. **Make sure `/movies/popular` is defined BEFORE `/movies/{movie_id}`** — explain in a comment why.
5. Add `GET /movies/search` with a **required** query param `q: str` that returns movies containing `q` (case-insensitive). (Also place it before the dynamic route.)

**Expected:**
- `/movies/popular` → the 3 popular movies (NOT a 422).
- `/movies/search` → 422 (q required).
- `/movies/search?q=the` → matching movies.

---

## Task 4 (Challenge) — Products API with validation + Enum
1. Define a Pydantic `Product` model (`id`, `name`, `price`, `category`) and a list of at least 5 products across 2–3 categories.
2. Add `GET /products/{product_id}` where `product_id` uses `Path(gt=0)`; return the product or an error message if not found.
3. Add `GET /products` with query params:
   - `category: str | None = None` — filter by category if provided,
   - `max_price: float | None = Query(default=None, gt=0)` — only products at or below this price,
   - `sort: SortOrder` **Enum** with values `asc` / `desc` (by price), default `asc`,
   - `limit: int = Query(default=10, ge=1, le=50)`.
4. Return the filtered, sorted, limited list plus a `count`.
5. Ensure the static `/products` route and the dynamic `/products/{product_id}` are ordered correctly.

**Expected at `/products?category=stationery&sort=desc&limit=2` (example):**
```json
{"count": 2, "items": [ ...two stationery products, priciest first... ]}
```

---

## Submission
Put your app in `params_api.py`, commit to repo `batch5-day14`, push to GitHub, and submit the link. Include a `README.md` with run instructions and a few example URLs to try.

## Grading checklist
- [ ] Path parameter with type conversion; bad type returns 422
- [ ] Pagination via optional query params with defaults
- [ ] Required vs optional query params demonstrated
- [ ] Static routes correctly placed BEFORE dynamic ones (with a comment explaining why)
- [ ] `Path()`/`Query()` constraints used and enforced
- [ ] An `Enum` restricts the sort value (dropdown in `/docs`)
