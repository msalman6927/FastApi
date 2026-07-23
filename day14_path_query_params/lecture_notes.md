# Day 14 — Path & Query Parameters

**Module:** 02 — FastAPI
**Duration:** 2 hours
**Prerequisite:** Day 13 (first FastAPI app, routes, docs), Day 11 (URLs: path vs query string)

> Where we are: Yesterday every route returned the same fixed thing. Real APIs are **dynamic** — `/users/5` gets user 5, `/users/9` gets user 9; `/items?limit=10` returns ten items. Today your API learns to **take input from the URL** two ways: **path parameters** (part of the path that identifies a resource) and **query parameters** (the `?key=value` bits for filtering/sorting/paginating). FastAPI validates and converts them automatically using the type hints you already know.
>
> **Instructor note:** This connects to Day 11's URL anatomy (path vs query string). The one genuinely tricky bit is **route order** (the gotcha I flagged on Day 13) — make sure you understand 1.3 before class.

---

# PART 1 — INSTRUCTOR DEEP-DIVE (teach yourself first)

## 1.1 Two ways a URL carries input

Recall from Day 11 the URL `https://api.site.com/users/5?sort=asc&limit=10`:
- **Path parameter:** `5` in `/users/5` — part of the path itself. Used to **identify a specific resource**.
- **Query parameters:** `sort=asc&limit=10` after the `?` — key=value pairs. Used to **filter, sort, paginate, or configure** a request.

Rule of thumb to teach: **path = *which* resource; query = *how* you want it** (filter/sort/limit). `/users/5` = "user 5". `/users?city=Karachi&limit=10` = "users, filtered to Karachi, at most 10".

## 1.2 Path parameters

You declare a path parameter with `{curly_braces}` in the route and a matching function argument:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):          # the name must match {user_id}
    return {"user_id": user_id}
```

What FastAPI does automatically (this is the magic):
- **Captures** the value from the URL: `/users/5` → `user_id = "5"`.
- **Converts** it to the declared type: because you wrote `user_id: int`, FastAPI turns `"5"` into the integer `5`.
- **Validates** it: `/users/abc` can't become an int → FastAPI returns a **422** with a clear error, and your function never runs. (Remember 422 from Days 11–12? Here it is again.)
- **Documents** it in `/docs` with the right type and an input box.

Teaching points:
- The `{name}` in the path and the function parameter name **must match exactly**.
- Declaring the type (`: int`) gives you free conversion + validation. Without it, you'd get a string.
- Try `/users/5` (works → 5), `/users/abc` (422). Show both live — the 422 is the "aha".

## 1.3 The route-order gotcha (the tricky bit — teach it carefully)

FastAPI matches routes **in the order they're defined, top to bottom**, and uses the **first** one that fits. This causes a classic bug when a **fixed** path and a **parameterized** path overlap:

```python
@app.get("/users/{user_id}")     # defined FIRST
def get_user(user_id: int): ...

@app.get("/users/me")            # defined SECOND - UNREACHABLE!
def get_me(): ...
```
Request `/users/me`: FastAPI checks `/users/{user_id}` first, tries to convert `"me"` to `int`, fails → **422**. It never reaches `/users/me`. The fix is **order**: put the **specific/fixed** routes *before* the **dynamic/parameterized** ones:
```python
@app.get("/users/me")            # specific first
def get_me(): ...

@app.get("/users/{user_id}")     # dynamic after
def get_user(user_id: int): ...
```
This is exactly the situation I flagged in Day 13's `05_practical_mini_api.py` (`/quotes/random` and `/quotes/count` before any `/quotes/{id}`). Now it has a name and a rule: **static routes before dynamic routes.** Demo the broken order live, watch it 422, then fix it — very memorable.

## 1.4 Query parameters

Any function parameter that is **not** part of the path becomes a **query parameter** automatically:

```python
@app.get("/items")
def list_items(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}
```
- `/items` → uses defaults: `limit=10, skip=0`.
- `/items?limit=5` → `limit=5, skip=0`.
- `/items?limit=5&skip=20` → `limit=5, skip=20`.

Key rules:
- **A parameter with a default value is an *optional* query parameter.** (`limit: int = 10` → optional, defaults to 10.)
- **A parameter with no default is a *required* query parameter.** Omit it → FastAPI returns 422 "field required".
- Types are converted/validated just like path params (`?limit=abc` → 422).
- To allow "not provided at all," make it optional/nullable: `q: str | None = None`.

```python
@app.get("/search")
def search(q: str, limit: int = 10):     # q required, limit optional
    return {"query": q, "limit": limit}
# /search            -> 422 (q is required)
# /search?q=python   -> {"query": "python", "limit": 10}
```

How FastAPI tells path vs query apart: **if the parameter name appears in the route's `{...}`, it's a path param; otherwise it's a query param.** Simple and automatic.

## 1.5 Combining path + query

Very common: identify a resource by path, then configure with query.
```python
@app.get("/users/{user_id}/orders")
def user_orders(user_id: int, status: str = "all", limit: int = 20):
    return {"user_id": user_id, "status": status, "limit": limit}
# /users/5/orders?status=shipped&limit=5
```
`user_id` is a path param (it's in `{}`); `status` and `limit` are query params (they're not). FastAPI sorts this out by name — you just declare them.

## 1.6 Adding validation & metadata: `Path()` and `Query()`

Type hints give basic validation. For **constraints** (ranges, lengths, patterns) and **docs metadata**, wrap defaults in `Path(...)` / `Query(...)` — the same idea as Pydantic's `Field()` from Day 12:

```python
from fastapi import FastAPI, Path, Query

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(gt=0, description="Must be a positive item id"),
    q: str | None = Query(default=None, min_length=3, max_length=50),
    limit: int = Query(default=10, ge=1, le=100),
):
    ...
```
- `Path(gt=0)` — the path param must be > 0; `/items/-1` → 422.
- `Query(min_length=3)` — the query string must be ≥ 3 chars.
- `Query(ge=1, le=100)` — bound a number's range.
- These constraints **show up in `/docs`** and are enforced automatically. It's Pydantic-style validation applied to URL inputs.

Note: `Query(default=None, ...)` (or `= None`) makes a query param optional; `Query(...)` with a literal `...` (Ellipsis) or no default makes it **required** even while adding constraints.

## 1.7 Restricting to specific values (Enum) — light touch

When a parameter should only accept certain values (e.g., `sort=asc|desc`), use an `Enum`:
```python
from enum import Enum
class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/items")
def list_items(sort: SortOrder = SortOrder.asc):
    return {"sort": sort.value}
```
FastAPI restricts input to the allowed values, returns 422 for anything else, and shows a **dropdown** in `/docs`. Show it briefly — it's a clean way to constrain inputs and it looks great in the docs. Don't over-invest today.

## 1.8 Path vs query — when to use which (design guidance)

| Use a PATH parameter when… | Use a QUERY parameter when… |
|----------------------------|------------------------------|
| identifying a specific resource | filtering, sorting, searching |
| it's required and hierarchical | it's optional / has a default |
| `/users/5`, `/posts/12/comments` | `?limit=10`, `?sort=asc`, `?q=python` |

RESTful instinct (from Day 11): the **resource identity** goes in the path (nouns), the **modifiers** go in the query. `/users/5/orders?status=shipped` reads naturally: "user 5's orders, filtered to shipped."

## 1.9 Common mistakes (warn students)

1. **Route order** — dynamic route defined before a fixed one shadows it (1.3). Static before dynamic.
2. **Path `{name}` not matching the function parameter name** → FastAPI error/empty. They must be identical.
3. **Forgetting the type hint** → the value stays a string (no conversion). Always annotate.
4. **Expecting an optional query param without a default** → it's *required*; add `= default` or `| None = None`.
5. **Confusing which is which** — if it's in `{}` it's a path param; otherwise query. Don't fight it.
6. **Passing the query in the path** or vice versa — `/items/10` won't fill `?limit=10`. Different mechanisms.
7. **`/docs` shows a required field they thought was optional** — check for a missing default.

## 1.10 Tricky student questions & your answers

**Q: "When do I use path vs query?"**
A: Path identifies *which* resource (`/users/5`); query configures *how* you want it (`?limit=10&sort=asc`). Required identity → path; optional modifiers → query.

**Q: "How does FastAPI know a parameter is path vs query?"**
A: If the name is inside the route's `{...}`, it's a path parameter; every other function parameter is a query parameter. Purely by name.

**Q: "Why did `/users/me` give me a 422?"**
A: A `/users/{user_id: int}` route was defined *before* it and matched first, trying to turn "me" into an int. Put fixed routes above dynamic ones.

**Q: "How do I make a query parameter optional?"**
A: Give it a default: `limit: int = 10`, or make it nullable: `q: str | None = None`. No default = required.

**Q: "What's the difference between `Query()` and Pydantic's `Field()`?"**
A: Same idea, different place. `Field()` validates model fields (request bodies); `Query()`/`Path()` validate URL parameters. Both give constraints + docs.

**Q: "Can a path parameter be optional?"**
A: Not really — it's part of the URL structure. If it's optional, it's usually a query parameter, or you make two routes. Path params are inherently required.

**Q: "Does the order of query parameters in the URL matter?"**
A: No. `?a=1&b=2` and `?b=2&a=1` are identical. FastAPI matches by name, not position. (Route *definition* order matters; query *param* order in the URL does not.)

---

# PART 2 — 2-HOUR LECTURE PLAN (minute-by-minute)

| Time | Segment | What you do |
|------|---------|-------------|
| **0–10 min** | **Recap + hook** | Recap Day 13 (routes return fixed data). "Today the API takes input." Recall Day 11's URL anatomy: path vs query string. |
| **10–35 min** | **Path parameters (live)** | `code/01_path_parameters.py`: `/users/{id}`, type conversion, `/users/5` (works) vs `/users/abc` (422). Show it in `/docs` with the input box. |
| **35–50 min** | **Route-order gotcha (live)** | `code/01`'s bonus section (or narrate): define `/users/{id}` before `/users/me`, watch `/users/me` 422, then reorder to fix. Name the rule: static before dynamic. |
| **50–75 min** | **Query parameters (live)** | `code/02_query_parameters.py`: defaults = optional, no default = required, `?limit=5&skip=10`, nullable `q`. Show the 422 for a missing required query. |
| **75–90 min** | **Combine + validate (live)** | `code/03_path_and_query_together.py` and `code/04_validation.py`: path+query in one route; `Path(gt=0)`, `Query(ge=1, le=100)`; constraints in `/docs`. |
| **90–108 min** | **Practical example + assignment** | `code/05_practical_items_api.py`: an items API with pagination + search + a sort Enum. Brief `assignments/assignment.md`. |
| **108–120 min** | **Q&A / buffer** | Test in `/docs`; troubleshoot; preview Day 15 (request bodies with POST). |

**Timing tip:** the route-order gotcha (35–50) is the single most valuable 15 minutes — it's a real bug students *will* hit, and seeing it break then fix is unforgettable. The 422 demos throughout keep reinforcing the validation story from Days 11–12. Encourage students to test everything in `/docs` "Try it out" rather than typing URLs by hand.

---

# PART 3 — CODE / DEMO FILES (in `code/`)

1. `01_path_parameters.py` — dynamic `{path}` params, type conversion, the route-order gotcha (with fix).
2. `02_query_parameters.py` — optional (default) vs required query params, nullable, multiple params.
3. `03_path_and_query_together.py` — combining path + query in one route.
4. `04_validation.py` — `Path()`/`Query()` constraints (`gt`, `ge`, `le`, `min_length`) and the 422s they produce.
5. `05_practical_items_api.py` — an items API with pagination, search, and a sort `Enum`.

**Install (if fresh venv):** `pip install "fastapi[standard]"`
**Run:** `fastapi dev 01_path_parameters.py` → open `http://127.0.0.1:8000/docs`.

---

# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
