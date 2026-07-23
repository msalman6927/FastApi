# Day 15 — Request Body (POST/PUT with Pydantic Models)

**Module:** 02 — FastAPI
**Duration:** 2 hours
**Prerequisite:** Day 12 (Pydantic), Day 13 (FastAPI), Day 14 (path/query params), Day 11 (HTTP methods, JSON)

> Where we are: So far the client sends input only through the **URL** (path + query). But to *create* or *update* things, the client must send a whole chunk of structured data — a new user, a new product. That data travels in the **request body** as JSON. Today FastAPI reads that JSON straight into a **Pydantic model** — the exact models you built on Day 12 — validating everything automatically. This is the moment Pydantic + FastAPI fully click together, and where your API becomes able to *write*, not just read.
>
> **Instructor note:** The single idea today: **declare a Pydantic model as a function parameter, and FastAPI fills it from the JSON body.** Everything else follows. Test with `/docs` "Try it out" — it gives you a JSON editor, so students don't need curl.

---

# PART 1 — INSTRUCTOR DEEP-DIVE (teach yourself first)

## 1.1 What is a request body? (recap + focus)

From Day 11: a request can carry a **body** — a payload of data — used mainly with **POST**, **PUT**, and **PATCH**. For APIs, the body is almost always **JSON**.

- **GET** requests: input via URL (path/query), **no body**.
- **POST/PUT/PATCH**: input via the **body** — the full object you're creating/updating.

Example: to create a user, the client sends
```
POST /users
Content-Type: application/json

{ "name": "Ayesha", "age": 25, "email": "ayesha@mail.com" }
```
The `{...}` is the body. Our job: receive it, validate it, use it.

## 1.2 The core idea: a Pydantic model IS the body

In FastAPI, you declare a **Pydantic model as a parameter**, and FastAPI:
1. Reads the raw JSON from the request body.
2. **Validates + converts** it against your model (Day 12 rules).
3. If invalid → returns **422** automatically with a precise error (your function never runs).
4. If valid → hands your function a clean, typed model object.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):          # the SHAPE of the expected body (Day 12)
    name: str
    age: int
    email: str

@app.post("/users")
def create_user(user: User):    # declare the model as a parameter -> it's the body
    # 'user' is a validated User object. Use it like any object.
    return {"message": f"Created {user.name}", "data": user}
```

**How does FastAPI know `user` is the body and not a query param?** The rule: **if a parameter's type is a Pydantic model, FastAPI reads it from the request body.** Simple types (`int`, `str`) with no `Path`/`Query` become query params; **Pydantic models become the body.** That's the whole mental model.

Compare to yesterday:
- `item_id: int` → path/query parameter (a single scalar from the URL).
- `user: User` (a model) → request body (a whole JSON object).

## 1.3 Testing it — `/docs` is your friend

Because POST bodies are awkward to send from a browser address bar, use the **interactive docs**:
1. Run `fastapi dev 01_first_post.py`, open `/docs`.
2. Find `POST /users`, click **"Try it out"**.
3. FastAPI shows an editable **JSON example** built from your model — edit it, click **Execute**.
4. See the response, status code, and even the equivalent `curl` command.

This is a huge teaching advantage — students send real POST requests with zero client code. Also show `requests.post(url, json={...})` from Python (Day 11) so they know how a *program* would call it. (curl is optional.)

## 1.4 What FastAPI generates for you (the payoff)

From that one model + route, FastAPI automatically:
- **Parses** the JSON body.
- **Validates** every field (types, required/optional, constraints from `Field()`).
- **Returns 422** with a clear, field-by-field error on bad data.
- **Documents** the expected body shape in `/docs`, with an example and a schema.
- **Gives editor autocomplete** on `user.` inside your function.

You wrote a model and a function; you got parsing + validation + docs + typing for free. Emphasize this — it's why FastAPI is loved.

## 1.5 Validation in action → 422

Because the body is a Pydantic model, all of Day 12's validation applies:
```python
class Product(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)
    in_stock: bool = True
```
- Missing `name` → 422 "field required".
- `price: -5` → 422 "Input should be greater than 0".
- `price: "abc"` → 422 "Input should be a valid number".
- Extra fields are ignored by default (configurable).

The 422 body is structured JSON listing each problem with its location — the client knows exactly what to fix. This is the same `ValidationError` from Day 12, now delivered over HTTP. Close the loop out loud: "Day 12 you saw this error in Python; today the client sees it as a 422."

## 1.6 Returning the created resource (and a 201 preview)

Convention: after a successful **POST** (create), return the created object, ideally with status **201 Created**:
```python
from fastapi import status

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    PRODUCTS.append(product)                # store it (in-memory for now)
    return product                          # return the created object as JSON
```
- `status_code=201` sets the response status (full status-code control is Day 16).
- Returning the model → FastAPI serializes it to JSON (Day 13).
- We store in an in-memory list today; a real database comes on Day 18. Full CRUD (list/get/update/delete together) is Day 17 — today we focus on *receiving bodies*.

## 1.7 Combining body + path + query

You can mix all three in one endpoint. FastAPI figures out each by its type/declaration:
```python
@app.put("/users/{user_id}")
def update_user(
    user_id: int,          # in {} -> PATH parameter
    user: User,            # Pydantic model -> BODY
    notify: bool = False,  # simple type, not in path -> QUERY parameter
):
    return {"updated": user_id, "data": user, "notify": notify}
# PUT /users/5?notify=true   with a JSON body
```
The rules stack cleanly:
- Name in `{}` → path.
- Pydantic model → body.
- Other simple parameter → query.

## 1.8 POST vs PUT (semantics recap from Day 11)

- **POST** `/users` → **create** a new resource (server assigns id). Not idempotent (POST twice = two resources).
- **PUT** `/users/5` → **update/replace** resource 5 entirely. Idempotent (PUT twice = same result).
- **PATCH** `/users/5` → partial update (change some fields). We'll touch PATCH lightly; PUT is the main one today.

For PUT you typically take **both** a path param (which resource) **and** a body (the new data) — see 1.7.

## 1.9 Nested bodies & lists (leverage Day 12)

Since the body is a Pydantic model, **nested models and lists just work** (Day 12):
```python
class Item(BaseModel):
    name: str
    qty: int

class Order(BaseModel):
    customer: str
    items: list[Item]          # a list of nested models

@app.post("/orders")
def create_order(order: Order):
    return {"customer": order.customer, "item_count": len(order.items)}
```
The client sends nested JSON; FastAPI validates the whole tree and gives you typed nested objects. This is how real payloads look.

## 1.10 Common mistakes (warn students)

1. **Sending the body as query/path** — a whole object goes in the JSON body, not the URL. If they try `/users?name=Ayesha&age=25`, FastAPI treats those as query params, not the model.
2. **Missing `Content-Type: application/json`** when calling manually (curl/other tools) → FastAPI may reject it. `/docs` and `requests(json=...)` set it for you.
3. **Sending malformed JSON** (single quotes, trailing commas) → 422/400. JSON needs double quotes (Day 11).
4. **Body shape doesn't match the model** (missing/extra/typed wrong) → 422. Read the error; it names the field.
5. **Declaring the model but expecting query behavior** — a Pydantic-model parameter is *always* the body. To get query params, use simple types.
6. **Trying to POST from the browser address bar** — you can't; address bars do GET. Use `/docs` or a client.
7. **Forgetting to store the data** — returning the object doesn't persist it; append to your list (or DB later).

## 1.11 Tricky student questions & your answers

**Q: "How does FastAPI know `user: User` is the body?"**
A: Because its type is a Pydantic model. Rule: Pydantic model parameter → request body; simple types → path/query. FastAPI decides by the type.

**Q: "Where does the validation come from?"**
A: From your Pydantic model (Day 12). FastAPI runs that model against the incoming JSON; failures become a 422 response automatically.

**Q: "Why 422 and not 400?"**
A: 400 = the request was malformed at a basic level; 422 = the JSON parsed fine but *failed validation* (wrong types, missing fields). FastAPI uses 422 for validation errors. (You saw this coming on Day 11.)

**Q: "How do I test a POST without writing a client?"**
A: `/docs` → "Try it out" gives a JSON editor and sends the real request. That's the fastest way. For code, `requests.post(url, json={...})`.

**Q: "Can I take a body and URL params together?"**
A: Yes — path params (in `{}`), the body (a model), and query params (simple types) can all coexist in one function. FastAPI sorts them by declaration.

**Q: "Does returning the object save it?"**
A: No. Returning just sends it back as JSON. To persist, store it (append to a list today, a database on Day 18).

**Q: "Can the body be a list of objects?"**
A: Yes — declare `items: list[Item]` inside a model, or even type the parameter as `list[Item]` directly. Nested/list bodies validate fully.

---

# PART 2 — 2-HOUR LECTURE PLAN (minute-by-minute)

| Time | Segment | What you do |
|------|---------|-------------|
| **0–10 min** | **Recap + hook** | Recap: URL input (Day 14) is fine for reading, but to *create* things we send a whole object. Show the `POST /users` JSON body example. |
| **10–35 min** | **First POST with a body (live)** | `code/01_first_post.py`: declare `user: User`, POST via `/docs` "Try it out". Show the auto-generated JSON editor + response. "The model IS the body." |
| **35–55 min** | **Validation → 422 (live)** | `code/02_body_validation.py`: constraints on the body; send bad JSON, read the 422. Tie back to Day 12's `ValidationError`. |
| **55–75 min** | **Store + return (201) + client call** | Extend to append to an in-memory list and return the created object with `status_code=201`. Show `requests.post(json=...)` from Python (`code/05` client section). |
| **75–95 min** | **Body + path + query together (live)** | `code/03_body_path_query.py` and `code/04_put_update.py`: PUT `/users/{id}` with a body + a query flag. Rules stack: path/body/query. |
| **95–108 min** | **Nested body + assignment** | `code/05_practical_notes_api.py`: a small notes/orders API with create + list, incl. a nested example. Brief `assignments/assignment.md`. |
| **108–120 min** | **Q&A / buffer** | Test in `/docs`; troubleshoot JSON mistakes; preview Day 16 (status codes & error handling). |

**Timing tip:** the make-or-break demo is the first POST via `/docs` (10–35) — students *see* FastAPI build a JSON form from their model and accept a real object. Then the 422 demo (35–55) reinforces validation. Have students actually break the body (wrong type, missing field) in "Try it out" and read the error themselves — active discovery beats watching.

---

# PART 3 — CODE / DEMO FILES (in `code/`)

1. `01_first_post.py` — declare a model as the body; first POST; test in `/docs`.
2. `02_body_validation.py` — `Field()` constraints on the body; the 422 responses.
3. `03_body_path_query.py` — combine body + path param + query param in one route.
4. `04_put_update.py` — PUT `/items/{id}` to replace, using path + body.
5. `05_practical_notes_api.py` — create + list notes in memory, a nested-body example, and a `requests` client snippet.

**Install (if fresh venv):** `pip install "fastapi[standard]"`
**Run:** `fastapi dev 01_first_post.py` → open `http://127.0.0.1:8000/docs` → "Try it out".

---

# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
