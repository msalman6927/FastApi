# Day 19 Assignment — Async & Dependencies

**Module 02 · Day 19**
**Goal:** Use dependencies to share logic across routes and write an async route.

---

## Task 1 (Easy) — An async route
1. Create an `async def` route `GET /wait` that `await asyncio.sleep(1)` then returns `{"status": "done"}`.
2. In a comment, explain the golden rule: when to use `async def` vs `def`.

---

## Task 2 (Medium) — Shared pagination dependency
1. Write a dependency `pagination(skip: int = 0, limit: int = 10)`.
2. Create two list routes (`/products`, `/orders`, each backed by a list of ~30 items) that both use `Depends(pagination)`.
3. Confirm both paginate correctly without duplicating the logic.

---

## Task 3 (Medium) — A guard dependency
1. Write a dependency `verify_token(token: str = Header(...))` that raises `HTTPException(401)` unless `token == "letmein"`.
2. Protect a `GET /dashboard` route with it (return some data on success).
3. Test with and without the correct header.

---

## Task 4 (Challenge) — Combine everything
1. Write a `yield` dependency `get_db()` that provides a simple in-memory list (setup) and prints a cleanup message after (teardown).
2. Write a `common_params` dependency combining `pagination` + an optional `q` search string (a sub-dependency composition).
3. `GET /notes` uses BOTH `get_db` and `common_params`, is protected by `verify_token`, and returns the filtered, paginated notes.

---

## Submission
`deps_app.py` → repo `batch5-day19` with a README.

## Checklist
- [ ] An async route using `await`
- [ ] A shared pagination dependency reused by ≥2 routes
- [ ] A guard dependency that returns 401 on bad/missing header
- [ ] A `yield` dependency with visible setup/cleanup
- [ ] A composed (sub-)dependency
