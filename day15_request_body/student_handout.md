# Day 15 Handout — Request Body (POST/PUT) (Keep This!)

## The one big idea
**Declare a Pydantic model as a function parameter → FastAPI fills it from the JSON request body**, validating automatically.
```python
class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):        # 'user' comes from the request BODY
    return {"created": user.name, "data": user}
```

## How FastAPI decides where a parameter comes from
| Parameter | Source |
|-----------|--------|
| name is in the path `{...}` | **path** parameter |
| type is a **Pydantic model** | request **body** |
| other simple type (int/str/bool) | **query** parameter |

## Testing a POST
Use `/docs` → find the endpoint → **"Try it out"** → edit the JSON example → **Execute**. No client code needed. (Address bars only do GET, so you can't POST from the URL bar.)
From code: `requests.post(url, json={...})`.

## Validation → 422 (from Day 12!)
The body is validated by your model. Bad data returns **422** with a precise error:
```json
POST /products  body {"name":"P","price":-5}
-> 422: name too short; price must be > 0
```
Same Pydantic `ValidationError` as Day 12, now sent over HTTP. Your function only runs if the body is valid.

## Return the created object (201)
```python
from fastapi import status
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create(product: Product):
    PRODUCTS.append(product)     # store it (in-memory today; DB on Day 18)
    return product               # returned model -> JSON
```

## Combine body + path + query
```python
@app.put("/users/{user_id}")
def update(user_id: int, user: User, notify: bool = False):
    ...   # user_id=path, user=body, notify=query
```

## POST vs PUT
- **POST** `/items` → **create** (server assigns id). Not idempotent.
- **PUT** `/items/5` → **replace** item 5 (you say which id). Idempotent.

## Nested bodies just work
```python
class Order(BaseModel):
    customer: str
    items: list[Item]           # list of nested models -> fully validated
```

## Top mistakes
- Trying to send a whole object via query/path (it goes in the JSON **body**).
- Malformed JSON (single quotes, trailing commas) → 422/400. JSON needs double quotes.
- Expecting a model parameter to be a query param (a model is ALWAYS the body).
- Returning the object doesn't **save** it — append to your list/DB.

## Your homework
`body_api.py`: create students, validated products (store + list), a tasks API with a PUT that mixes path+body+query, and a nested shopping-cart body. Push to repo `batch5-day15` with a README.

## Next class (Day 16)
**Response models, status codes & error handling** — control exactly what your API returns and its status code, and raise clean errors like **404 Not Found** with `HTTPException`.
