# Day 13 — FastAPI Intro (First App, Uvicorn, Path Operations, Auto Docs)

**Module:** 02 — FastAPI
**Duration:** 2 hours
**Prerequisite:** Day 11 (HTTP/REST), Day 12 (Pydantic), OOP module

> Where we are: You understand HTTP (request→response→status→JSON) and Pydantic (validate data). Today they **combine**: you build and run your own **web API** with FastAPI. By the end of class every student has a live server running on their laptop, returning JSON, with **automatic interactive documentation** they can click through in a browser. This is the moment the course turns from "scripts" to "software other programs can talk to."
>
> **Instructor note:** FastAPI is a weak area for you, so Part 1 is detailed. The two things to be 100% solid on before class: (1) the difference between **uvicorn** (the server) and **FastAPI** (the framework), and (2) how to **run** an app and reach the **auto docs**. Practice running one app yourself before you teach.

---

# PART 1 — INSTRUCTOR DEEP-DIVE (teach yourself first)

## 1.1 What is FastAPI, and why it?

**FastAPI** is a modern Python framework for building web APIs. You write Python functions; FastAPI turns them into HTTP endpoints that clients (browsers, apps, AI agents) can call.

Why it's the right choice for this course:
- **Built on Pydantic** — the models you learned yesterday *are* how FastAPI validates requests. Nothing new to learn there.
- **Automatic interactive docs** — it generates a clickable API documentation site for free (Swagger UI). Huge for learning and testing.
- **Type-hint driven** — you declare types; FastAPI validates, converts, and documents automatically.
- **Fast & async-ready** — high performance; async support for I/O-heavy work (like calling LLMs later).
- **Industry standard for AI** — most Python AI/LLM services expose FastAPI endpoints. LangGraph/RAG apps you build later will often be wrapped in FastAPI.

Mental model: **FastAPI is how you build the "kitchen"** (server) from Day 11's restaurant analogy — the thing that receives orders (requests) and sends back food (responses).

## 1.2 The two pieces: framework vs server (uvicorn)

This confuses everyone, so nail it: you need **two** things working together.

1. **FastAPI (the framework):** the library where you *write* your API logic — the routes, the data handling. It defines *what* your API does. But FastAPI by itself can't listen for requests on the network.
2. **Uvicorn (the server):** the program that actually **runs** your app, listens on a network port, receives raw HTTP requests, and hands them to FastAPI. It's the "engine" that makes your app reachable.

Analogy: **FastAPI is the restaurant's recipes and staff (the logic); uvicorn is the building with a front door and address where customers actually arrive.** Recipes alone serve no one — you need the open building. That's why we run `uvicorn` (or `fastapi dev`) rather than just `python file.py` in production.

Technical note (light): uvicorn is an **ASGI** server (Asynchronous Server Gateway Interface — the modern async standard). You don't need ASGI details today; just know uvicorn is the server that runs FastAPI apps.

## 1.3 Your first app (three lines that matter)

```python
from fastapi import FastAPI      # 1. import the framework

app = FastAPI()                  # 2. create the application object

@app.get("/")                    # 3. a "path operation": GET requests to "/"
def read_root():
    return {"message": "Hello, Batch 5!"}   # returned dict -> JSON automatically
```

Decode each part:
- `app = FastAPI()` — creates the central application object. **The name `app` matters** because we tell the server to run *this* object (`uvicorn file:app`).
- `@app.get("/")` — a **decorator** that registers the function below as the handler for **GET** requests to the **path** `/`. This is called a **path operation** (path = the URL, operation = the HTTP method).
- The function returns a Python `dict`; FastAPI **automatically converts it to JSON** and sends it as the response body with status 200. No manual `json.dumps` needed.

That's a complete, working API. Everything else is variations on this.

## 1.4 Running the app + reaching it

**Install (once):**
```
pip install "fastapi[standard]"
```
This pulls in FastAPI, uvicorn, and the handy `fastapi` command-line tool.

**Run it — recommended (beginner-friendly, auto-reload):**
```
fastapi dev 01_hello_fastapi.py
```
`fastapi dev <path>` starts the server in development mode with **auto-reload** (it restarts when you save changes). It takes a *file path*, so our numbered filenames work fine.

**Run it — the classic way (know this too):**
```
uvicorn 01_hello_fastapi:app --reload
```
Read this as `uvicorn <module>:<app-object> --reload`. `--reload` = restart on save. (If a student's system objects to the leading digit in the module name, `fastapi dev 01_hello_fastapi.py` always works, or they can run `python 01_hello_fastapi.py` using the `__main__` block we include.)

**Reach it in the browser:**
- The server prints something like `Uvicorn running on http://127.0.0.1:8000`.
- `127.0.0.1` = **localhost** = "this same computer." `8000` = the **port** (the "door number" the server listens on).
- Open `http://127.0.0.1:8000/` → you see your JSON.
- Open `http://127.0.0.1:8000/docs` → the **interactive documentation** (the star of the day, 1.7).

**Stop the server:** `Ctrl + C` in the terminal.

## 1.5 Path operations (routes) in depth

A **path operation** = a **path** (URL) + an **operation** (HTTP method) + the function that handles it.

```python
@app.get("/")            def home(): ...          # GET /
@app.get("/about")       def about(): ...         # GET /about
@app.get("/items")       def list_items(): ...    # GET /items
@app.post("/items")      def create_item(): ...   # POST /items
```

Teaching points:
- The decorator's method (`.get`, `.post`, `.put`, `.delete`, `.patch`) sets **which HTTP verb** the route responds to — connecting directly to Day 11's methods/CRUD.
- The string (`"/about"`) is the **path**.
- The **function name is yours** (`home`, `about`) — it doesn't affect the URL. The URL comes from the decorator path, not the function name. (Beginners often think the function name is the route — correct them.)
- Two functions can share a path with **different methods** (`GET /items` vs `POST /items`) — that's RESTful design from Day 11.

## 1.6 Returning data — automatic JSON serialization

Whatever your function returns, FastAPI turns into a JSON response:
```python
@app.get("/dict")   def d(): return {"a": 1}          # -> {"a": 1}
@app.get("/list")   def l(): return [1, 2, 3]         # -> [1,2,3]
@app.get("/str")    def s(): return "hello"           # -> "hello"
@app.get("/user")   def u(): return User(name="Ayesha", age=25)  # Pydantic model -> JSON
```
- Python `dict`/`list`/`str`/`int`/`bool` → JSON automatically.
- **Pydantic models are serialized automatically too** (FastAPI calls `model_dump()` for you). This is the direct link to yesterday: return a model, get clean JSON. You'll use this constantly.
- Default status code is **200**; you can change it (Day 16).

## 1.7 The automatic interactive docs (the "wow" moment)

FastAPI reads your routes and types and **auto-generates a live documentation website** — no extra work. Two URLs:
- **`/docs`** — **Swagger UI**: an interactive page listing every endpoint, with a **"Try it out"** button that sends real requests from the browser. Students can test the API without writing any client code.
- **`/redoc`** — **ReDoc**: a cleaner, read-only documentation view of the same API.
- **`/openapi.json`** — the raw **OpenAPI schema** (a JSON description of your whole API) that both docs pages are built from. (OpenAPI is an industry-standard format for describing APIs.)

Why this is a big deal: normally documenting and providing a test client for an API is tedious manual work. FastAPI gives it to you for free, always in sync with your code. **Spend real class time clicking through `/docs`** — it's the feature that makes students love FastAPI and it's how they'll test everything for the rest of the module.

You can enrich the docs with `summary`, `description`, and `tags` on each route, and Pydantic `Field(description=...)` — a nice preview of professional API docs.

## 1.8 The development workflow

- Start with `fastapi dev <file>` (auto-reload on).
- Edit code → save → the server **reloads automatically** → refresh `/docs` to see changes.
- Keep the terminal visible: errors (tracebacks) print there.
- `Ctrl+C` to stop.
This tight loop (edit → save → refresh) is how you'll work all module. `--reload`/`fastapi dev` is a **development** convenience; in the deployment module we run without reload for production.

## 1.9 `async def` vs `def` (light touch — full treatment Day 19)

You'll see both `def` and `async def` for route functions online. For today:
- **`def` works perfectly** — FastAPI runs it correctly. Use plain `def` now.
- `async def` is for later, when a route does I/O that can "await" (calling an LLM, a database, another API) without blocking. We cover it properly on Day 19.
Don't rabbit-hole here; just reassure students that `def` is fine and `async` comes later.

## 1.10 Common mistakes (warn students)

1. **Running `python file.py` and expecting a server** — without a `__main__`/uvicorn block, nothing happens. Use `fastapi dev file.py` (our files also include a `__main__` fallback so `python file.py` works).
2. **Wrong `module:app` name** in the uvicorn command — the part after `:` must match the variable (`app = FastAPI()`). If they named it `application`, it's `file:application`.
3. **Forgetting to save** before checking — with reload, you must save to trigger the restart.
4. **Port already in use** (`Address already in use`) — a previous server is still running. `Ctrl+C` it, or run on another port: `fastapi dev file.py --port 8001`.
5. **Thinking the function name is the URL** — the URL is the decorator's path string, not the function name.
6. **Editing but seeing old output** — either reload isn't on (use `fastapi dev`/`--reload`) or the browser cached; hard-refresh.
7. **Missing decorator** — a function without `@app.get(...)` is never reachable as a route.

## 1.11 Tricky student questions & your answers

**Q: "Why do I need uvicorn? Isn't FastAPI enough?"**
A: FastAPI is the *code* of your API; uvicorn is the *server* that runs it and listens for network requests. Framework + server. The recipes need a building with a door.

**Q: "What's `127.0.0.1:8000`?"**
A: `127.0.0.1` (localhost) means "this computer"; `8000` is the port your server listens on. It's the address to reach your API from the same machine. Others on your network would use your machine's IP.

**Q: "How do people on the internet reach my API?"**
A: Not yet — right now it's only on your laptop (localhost). In the deployment module we put it on a real server with a public address. Today is local development.

**Q: "How is `/docs` generated? Did I write it?"**
A: No — FastAPI reads your routes and type hints and builds the OpenAPI schema, then renders Swagger UI from it. Free and always in sync with your code.

**Q: "Do I have to use `async def`?"**
A: No. Plain `def` works great and is what we use now. `async def` matters when a route awaits I/O; we cover it on Day 19.

**Q: "Where do I put multiple endpoints — one file or many?"**
A: For now, one file is fine. As it grows we'll split into routers and a project structure (Day 21).

**Q: "Is FastAPI a web *server*?"**
A: No — it's a *framework*. Uvicorn is the server. People say "run the FastAPI server" loosely, but technically uvicorn serves your FastAPI app.

---

# PART 2 — 2-HOUR LECTURE PLAN (minute-by-minute)

| Time | Segment | What you do |
|------|---------|-------------|
| **0–10 min** | **Recap + kickoff** | Recap HTTP (Day 11) + Pydantic (Day 12). "Today we BUILD the kitchen." Install: `pip install "fastapi[standard]"`. Confirm everyone's install works. |
| **10–30 min** | **First app + RUN it (live)** | `code/01_hello_fastapi.py`. Explain the 3 key lines. Run `fastapi dev 01_hello_fastapi.py`. Open `127.0.0.1:8000/` → JSON. **Everyone gets a server running.** Handle port/errors live. |
| **30–45 min** | **The auto docs (live, the wow)** | Open `/docs`. Click "Try it out", "Execute". Show `/redoc` and `/openapi.json`. Let students explore their own. |
| **45–70 min** | **Multiple routes & path operations** | `code/02_multiple_routes.py`: several GET routes; function name ≠ URL; edit a route, save, watch reload, refresh docs. Reinforce path vs method. |
| **70–95 min** | **Returning data (dicts, lists, models)** | `code/03_returning_data.py`: dict/list/str → JSON; **return a Pydantic model → JSON** (link to Day 12). `code/04_docs_metadata.py` for tags/summary in docs. |
| **95–110 min** | **Practical mini-API + assignment** | `code/05_practical_mini_api.py`: a small multi-route API. Brief `assignments/assignment.md`. |
| **110–120 min** | **Q&A / buffer** | Troubleshoot installs/ports; make sure everyone can start a server and reach `/docs`. |

**Timing tip:** the two make-or-break moments are (1) *every student successfully running a server and seeing JSON* (10–30) and (2) *playing with `/docs`* (30–45). Budget extra buffer for install/port issues — on Windows the first-time `pip install "fastapi[standard]"` and firewall prompt can eat time. If someone's stuck, pair them with a neighbor and keep moving; the auto-docs demo is worth protecting.

---

# PART 3 — CODE / DEMO FILES (in `code/`)

1. `01_hello_fastapi.py` — the minimal first app (one GET route). Run this first.
2. `02_multiple_routes.py` — several routes; path vs method; function-name ≠ URL.
3. `03_returning_data.py` — dict/list/str and **Pydantic model** responses → JSON.
4. `04_docs_metadata.py` — enrich the auto docs with `tags`, `summary`, `description`.
5. `05_practical_mini_api.py` — a small multi-route "quotes/catalog" API to tie it together.

**Install command needed today:**
```
pip install "fastapi[standard]"
```
**Run any file (recommended):** `fastapi dev 01_hello_fastapi.py` then open `http://127.0.0.1:8000/docs`.
**Or:** `uvicorn 01_hello_fastapi:app --reload` — **or** `python 01_hello_fastapi.py` (each file has a `__main__` fallback).

---

# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
