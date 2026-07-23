# Day 21 — Project Structure (Routers, Folders, `.env` Config)

**Module:** 02 — FastAPI | **Duration:** 2 hours
**Prerequisite:** Days 13–20; Day 1 (`.gitignore`, venv)

> Where we are: Everything so far lived in one file. Real apps have dozens of routes, models, and settings — one file becomes unmaintainable. Today you learn to **organize a FastAPI project** professionally: split routes with **`APIRouter`**, use a sensible **folder structure**, and manage configuration/secrets with **`.env`** files (where the JWT secret from Day 20 belongs). This is how production apps — and the capstone — are laid out.
>
> **Instructor note:** This is an organizational lesson. The concepts are simple; the value is a clean template students reuse for the rest of the course. Have them build the structure by hand once.

---

# PART 1 — INSTRUCTOR DEEP-DIVE

## 1.1 Why structure? The single-file problem
A 500-line `main.py` with all routes, models, DB code, and config is hard to read, hard to test, and causes merge conflicts in teams. Splitting by responsibility gives:
- **Readability** — find things fast.
- **Reusability** — shared config/db in one place.
- **Team-friendliness** — people work on different files.
- **Testability** — isolate pieces.

## 1.2 `APIRouter` — splitting routes into modules
`APIRouter` is a "mini-FastAPI" you can define in its own file, then plug into the main app. Group related routes (all `/users` endpoints in `users.py`, all `/items` in `items.py`).
```python
# routers/users.py
from fastapi import APIRouter
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")            # becomes GET /users/
def list_users(): ...

@router.get("/{user_id}")   # becomes GET /users/{user_id}
def get_user(user_id: int): ...
```
```python
# main.py
from fastapi import FastAPI
from .routers import users, items
app = FastAPI()
app.include_router(users.router)   # plug the router in
app.include_router(items.router)
```
- `prefix="/users"` prepends to every route in that file — no repetition.
- `tags=["users"]` groups them in `/docs`.
- `include_router` mounts them onto the app. Clean separation.

## 1.3 A sensible folder structure
A common, scalable layout (build this today):
```
myapp/
├── __init__.py          # marks the folder as a Python package
├── main.py              # creates the app, includes routers
├── config.py            # settings loaded from .env
├── database.py          # engine + get_session (Day 18) [optional today]
├── models.py            # Pydantic / SQLModel models
└── routers/
    ├── __init__.py
    ├── users.py         # user routes (APIRouter)
    └── items.py         # item routes (APIRouter)
.env                     # secrets & config (NOT committed)
.env.example             # template (committed) showing needed keys
requirements.txt
```
Principles: **separate by responsibility** (routes vs models vs config vs db). Start simple; grow as needed. `__init__.py` files make folders importable packages.

## 1.4 Environment variables & `.env` (config + secrets)
Hardcoding secrets (JWT secret, DB URL, API keys) in code is dangerous and inflexible. Instead, put them in a **`.env` file** and load them at runtime.
```
# .env  (never commit this - it's in .gitignore)
JWT_SECRET=super-long-random-secret
DATABASE_URL=sqlite:///app.db
DEBUG=true
```
**`pydantic-settings`** (from the Pydantic family) loads and validates these into a typed settings object:
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str
    database_url: str = "sqlite:///app.db"
    debug: bool = False
    model_config = {"env_file": ".env"}

settings = Settings()      # reads .env + real environment variables
```
Now anywhere: `from .config import settings; settings.jwt_secret`. Benefits:
- **Typed & validated** (it's Pydantic — Day 12): a missing required var fails loudly at startup.
- **Environment-specific**: different `.env` for dev/prod without code changes.
- **Secrets stay out of code and git.**

## 1.5 `.env` and Git (the security rule)
- **`.env` must be in `.gitignore`** (Day 1) — never commit real secrets. A leaked secret on GitHub is stolen within minutes.
- Commit a **`.env.example`** with the *keys* but dummy values, so teammates know what to set.
This is the professional secrets pattern; the capstone will use it.

## 1.6 Where earlier pieces live now
- JWT `SECRET` (Day 20) → `.env` → `settings.jwt_secret`.
- DB engine + `get_session` (Day 18) → `database.py`.
- Models (Days 12–18) → `models.py`.
- Auth dependencies (Days 19–20) → `dependencies.py` or an `auth.py` module.
Everything you've learned slots into a clean home.

## 1.7 Common mistakes
1. Committing `.env` with real secrets (put it in `.gitignore`; commit `.env.example` instead).
2. Missing `__init__.py` → import errors (`ModuleNotFoundError`).
3. Wrong import style — use package-relative imports (`from .config import settings`) inside the package.
4. Recreating `Settings()` everywhere — create it once and import the instance.
5. Router `prefix` duplicated in the route path (don't repeat `/users` inside the router if the prefix already adds it).
6. Running from the wrong directory so the package isn't importable (run from the folder containing the package).

## 1.8 Tricky questions
- **"How do I run a packaged app?"** `fastapi dev myapp/main.py`, or `uvicorn myapp.main:app --reload` from the folder above the package.
- **"Why not just import os.getenv?"** You can, but `pydantic-settings` adds typing, validation, defaults, and one place for all config.
- **"How many files is right?"** Enough to keep each focused; don't over-split a tiny app. Grow the structure with the project.
- **"Do env vars override `.env`?"** Yes — real environment variables take precedence, which is how production injects secrets without a file.

---

# PART 2 — 2-HOUR LECTURE PLAN

| Time | Segment | Action |
|------|---------|--------|
| 0–10 | Recap + hook | Show a bloated single-file app; "this doesn't scale." |
| 10–35 | APIRouter (live) | `code/01_single_file_problem.py` → refactor routes into `myapp/routers/`. |
| 35–65 | Build the structure (live) | Create `myapp/` package: `main.py`, `routers/users.py`, `routers/items.py`, `include_router`. Run it. |
| 65–95 | Config & .env (live) | `config.py` with `pydantic-settings`; `.env` + `.env.example`; `.gitignore`. Move a secret into `.env`. |
| 95–110 | Wire it together + assignment | Full run via `fastapi dev myapp/main.py`; brief assignment. |
| 110–120 | Q&A / buffer | Preview Day 22 (revision + mini-project using this structure). |

**Tip:** build the folder tree live, file by file, explaining each file's single responsibility. The payoff is a reusable template — students should save it. Emphasize the `.gitignore` + `.env.example` habit (real-world security).

---

# PART 3 — CODE FILES (`code/`)
1. `01_single_file_problem.py` — the "everything in one file" anti-pattern (motivation).
2. `myapp/` — a properly structured package: `main.py`, `config.py`, `routers/users.py`, `routers/items.py`, `__init__.py` files.
3. `myapp/.env.example` + a `.gitignore` — the config/secrets pattern.

**Install:** `pip install "fastapi[standard]" pydantic-settings`
**Run:** from the `code/` folder: `fastapi dev myapp/main.py` (create a real `.env` from `.env.example` first) → `/docs`.

---

# PART 4 — STUDENT HANDOUT (recap)
- **`APIRouter`** splits routes into modules: `router = APIRouter(prefix="/users", tags=["users"])`, then `app.include_router(users.router)`.
- **Folder structure:** separate `main.py`, `config.py`, `models.py`, `database.py`, `routers/`. `__init__.py` makes folders packages.
- **`.env` + `pydantic-settings`** for typed config/secrets: `class Settings(BaseSettings)` with `env_file=".env"`; use `settings.jwt_secret`.
- **`.env` is git-ignored**; commit `.env.example` (keys, dummy values). Never commit real secrets.
- Run a package: `fastapi dev myapp/main.py`.
- Homework: restructure a previous app into a package with routers + `.env`. Push to `batch5-day21`.
- **Next (Day 22):** FastAPI revision + mini-project — a complete, structured Notes/Tasks API with DB, auth, and clean layout.
