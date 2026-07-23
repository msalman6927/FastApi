# Day 13 Handout — FastAPI Intro (Keep This!)

## Two pieces you need
- **FastAPI** = the **framework** — where you write your API code.
- **Uvicorn** = the **server** — the program that runs your app and listens for requests.
Analogy: FastAPI is the recipes + staff; uvicorn is the building with a front door.

## The minimal app
```python
from fastapi import FastAPI

app = FastAPI()                 # the application object (name matters!)

@app.get("/")                   # a "path operation": GET requests to "/"
def read_root():
    return {"message": "Hello!"}  # dict -> JSON automatically
```

## Install & run
```
pip install "fastapi[standard]"
fastapi dev app.py               # recommended: auto-reload on save
# or: uvicorn app:app --reload    # module:app-object
# or: python app.py               # if the file has a __main__ block
```
Then open:
- `http://127.0.0.1:8000/` → your JSON
- `http://127.0.0.1:8000/docs` → **interactive Swagger docs** ⭐
- `http://127.0.0.1:8000/redoc` → alternate docs
Stop with **Ctrl + C**. (`127.0.0.1` = this computer; `8000` = the port.)

## Path operations (routes)
```python
@app.get("/about")     def about(): ...    # GET /about
@app.post("/items")    def create(): ...   # POST /items
```
- The **decorator method** (`.get`/`.post`/...) = the HTTP verb (Day 11).
- The **decorator string** = the URL path.
- The **function name does NOT affect the URL** — only the decorator path does.

## Returning data → JSON automatically
Return a `dict`, `list`, `str`, `bool`, or a **Pydantic model** — FastAPI serializes it to JSON for you (status 200 by default).
```python
@app.get("/product")
def get_product():
    return Product(name="Pen", price=50)   # Pydantic model -> JSON
```

## The auto docs (the killer feature)
FastAPI reads your routes + type hints and builds a live docs site for free:
- `/docs` — Swagger UI with a **"Try it out"** button to send real requests.
- `/redoc` — clean read-only docs.
- `/openapi.json` — the raw API schema both are built from.
Enrich it: `FastAPI(title=..., version=...)`, and per-route `tags=[...]`, `summary=...`, plus the function's docstring as the description.

## `def` vs `async def`
Use plain `def` for now — it works perfectly. `async def` is for later (Day 19), when a route awaits I/O like an LLM or database.

## Top mistakes
- `python file.py` with no `__main__` block → nothing runs. Use `fastapi dev file.py`.
- Wrong `module:app` name in the uvicorn command.
- Forgetting to **save** (reload triggers on save).
- "Port already in use" → Ctrl+C the old server or use `--port 8001`.
- Thinking the function name is the URL (it's the decorator path).

## Your homework
Build `app.py`: a welcome route, an `/about` with metadata, a `/courses` returning Pydantic models, and a read-only mini Task Manager with filter routes. Push to repo `batch5-day13` with a README. (Details in `assignments/assignment.md`.)

## Next class (Day 14)
**Path & query parameters** — make routes *dynamic*: `/users/{id}` to fetch a specific user, and `/items?limit=10` to filter. Your API starts taking input.
