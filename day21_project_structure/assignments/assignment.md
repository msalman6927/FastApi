# Day 21 Assignment — Project Structure

**Module 02 · Day 21**
**Goal:** Restructure an API into a clean package with routers and `.env` config.

> `pip install "fastapi[standard]" pydantic-settings`

---

## Task 1 (Core) — Build the package
Create this structure:
```
blogapp/
├── __init__.py
├── main.py
├── config.py
└── routers/
    ├── __init__.py
    ├── posts.py
    └── comments.py
```
- `posts.py`: an `APIRouter(prefix="/posts")` with GET all / GET one (404) / POST.
- `comments.py`: an `APIRouter(prefix="/comments")` with GET all / POST.
- `main.py`: create the app and `include_router` both.
- Run with `fastapi dev blogapp/main.py` and confirm `/docs` groups posts and comments.

---

## Task 2 (Medium) — Config via .env
1. `config.py`: a `Settings(BaseSettings)` with `app_name`, `admin_email`, `debug` reading from `.env`.
2. Create `.env` (real) and `.env.example` (template).
3. Use `settings.app_name` as the FastAPI `title`.
4. Add a `.gitignore` that ignores `.env`.

---

## Task 3 (Medium) — Shared dependency module
1. Add `dependencies.py` with a `pagination` dependency (Day 19).
2. Use it in both routers' "list" endpoints.

---

## Task 4 (Challenge) — Persisted + structured
1. Add `database.py` (engine + `get_session`, Day 18) and make `posts` persist in SQLite.
2. Keep models in a `models.py`.
3. Full CRUD for posts across the structured package, config-driven DB URL from `.env`.

---

## Submission
The `blogapp/` package → repo `batch5-day21` with a README (structure diagram + run command). Ensure `.env` is NOT committed but `.env.example` is.

## Checklist
- [ ] Routes split into `APIRouter` modules with prefixes/tags
- [ ] `main.py` stays small and includes routers
- [ ] `pydantic-settings` config from `.env`
- [ ] `.env` git-ignored; `.env.example` committed
- [ ] (Challenge) DB + models in their own modules
