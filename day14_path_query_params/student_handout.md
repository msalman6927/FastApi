# Day 14 Handout — Path & Query Parameters (Keep This!)

## Two ways a URL carries input
`https://api.site.com/users/5?sort=asc&limit=10`
- **Path parameter** (`5`) — identifies **which** resource.
- **Query parameters** (`sort=asc&limit=10`) — configure **how** you want it (filter/sort/paginate).

## Path parameters
```python
@app.get("/users/{user_id}")
def get_user(user_id: int):        # name must match {user_id}
    return {"user_id": user_id}
```
- `{name}` in the path → function argument of the same name.
- The type hint (`: int`) auto-converts and validates. `/users/abc` → **422**.

## ⚠️ The route-order gotcha
FastAPI matches routes **top-to-bottom**, first match wins. Put **static routes BEFORE dynamic ones**:
```python
@app.get("/users/me")          # specific FIRST
def me(): ...
@app.get("/users/{user_id}")   # dynamic AFTER
def user(user_id: int): ...
```
If reversed, `/users/me` tries to become an int → 422, never reaching the `me` route.

## Query parameters
Any function parameter **not** in the path is a query parameter.
```python
@app.get("/items")
def list_items(limit: int = 10, skip: int = 0):   # both optional (have defaults)
    ...
```
- **Default value → optional.** **No default → required** (missing it → 422).
- Nullable/optional: `q: str | None = None`.
- URL order of query params doesn't matter: `?a=1&b=2` == `?b=2&a=1`.

## Combine path + query
```python
@app.get("/users/{user_id}/orders")
def orders(user_id: int, status: str = "all", limit: int = 20):
    ...   # user_id=path (in {}), status/limit=query (not in {})
```

## Validation with Path() / Query()
Like Pydantic's `Field()`, but for URL inputs:
```python
from fastapi import Path, Query
item_id: int = Path(gt=0)
limit: int = Query(default=10, ge=1, le=100)
q: str | None = Query(default=None, min_length=3)
```
Constraints are enforced (→ 422) **and** shown in `/docs`.

## Restrict values with an Enum (dropdown in docs)
```python
from enum import Enum
class SortBy(str, Enum):
    asc = "asc"; desc = "desc"

@app.get("/items")
def items(sort: SortBy = SortBy.asc): ...
```

## Path vs query — which to use
| Path | Query |
|------|-------|
| identify a resource (`/users/5`) | filter/sort/search (`?limit=10`) |
| required, hierarchical | optional / has a default |

## Top mistakes
- Dynamic route before a fixed one (order!).
- `{name}` not matching the function parameter name.
- Forgetting the type hint (value stays a string).
- Expecting an optional query param without a default (it's required).

## Your homework
`params_api.py`: dynamic book lookup, pagination, a search route with correct ordering, and a Products API with `Path()`/`Query()` validation + a sort Enum. Push to repo `batch5-day14` with a README.

## Next class (Day 15)
**Request bodies with POST** — accept JSON data from clients using your Pydantic models as the request body. Your API starts *creating* things, not just reading.
