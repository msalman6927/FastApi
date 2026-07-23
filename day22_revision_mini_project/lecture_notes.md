# Day 22 — FastAPI Revision + Mini-Project (Task Manager API)

**Module:** 02 — FastAPI (FINAL DAY) | **Duration:** 2 hours
**Prerequisite:** Days 11–21 (all of FastAPI)

> Where we are: The capstone of Module 2. Two jobs: (1) **revise** the whole FastAPI module, and (2) build one **complete, structured, database-backed, authenticated API** — a **Task Manager** — that uses every concept together. Students leave with a real, production-shaped backend for their portfolio and a template they'll reuse for the capstone. Like the OOP mini-project day, this is a **guided build**, not new theory.

---

# PART 1 — INSTRUCTOR REVISION (the module on one page)

| Day | Concept | One line |
|-----|---------|----------|
| 11 | HTTP/REST | request→response, methods, status codes, JSON |
| 12 | Pydantic | declare + validate data with models |
| 13 | FastAPI intro | `app`, routes, `/docs`, uvicorn |
| 14 | Path/query params | dynamic URLs, filtering, route order |
| 15 | Request body | Pydantic model = the JSON body |
| 16 | response_model/status/errors | shape output, correct codes, `HTTPException` |
| 17 | CRUD | the 5-route resource pattern |
| 18 | Databases | SQLModel + SQLite persistence |
| 19 | Async/deps | `Depends`, `async def`, session dependency |
| 20 | Auth | API keys, JWT login, hashed passwords |
| 21 | Structure | routers, folders, `.env` config |

**The through-line:** you can now build a **secure, persistent, well-structured REST API** — the backbone of any web/AI backend. Agents (Module 3) will be wrapped in exactly this.

## 1.1 The mini-project: Task Manager API — build map
A multi-user task manager where each user manages their own tasks. Every concept has a home:

| Piece | Concepts (days) |
|-------|-----------------|
| `config.py` (`.env`) | config/secrets (21) |
| `database.py` (engine + `get_session`) | DB + dependency (18, 19) |
| `models.py` (`User`, `Task`, In/Out models) | Pydantic + SQLModel + response models (12, 16, 18) |
| `auth.py` (hash, JWT, `get_current_user`) | auth (20), dependencies (19) |
| `routers/auth_routes.py` (register/login) | body, status, errors (15, 16), auth (20) |
| `routers/tasks.py` (CRUD, per-user) | CRUD (17), params (14), DB (18), auth guard (19–20) |
| `main.py` (`include_router`) | structure (21) |

Narrate each concept as you assemble it: "here's the JWT dependency from Day 20 guarding the tasks router… here's the SQLModel session from Day 18…".

## 1.2 Design decisions to explain
- **Per-user isolation:** every task has a `user_id`; the tasks router filters by the current user (from the JWT). Users never see others' tasks — authorization by identity.
- **Input/output models:** `TaskCreate` (no id/user), `TaskPublic` (safe output). The DB `Task` table stays internal.
- **The auth guard as a dependency:** `get_current_user` runs before task routes; no token → 401. This is why dependencies (Day 19) came before auth (Day 20).
- **`.env` for the JWT secret + DB URL:** never hardcoded; committed as `.env.example`.

## 1.3 Common build pitfalls (pre-empt)
- Forgetting `create_all` at startup → "no such table".
- Not filtering tasks by `user_id` → users see everyone's tasks (security bug).
- Committing `.env` → leaked secret. `.gitignore` it.
- Returning the DB model with sensitive fields → use `response_model`.
- Route order in the tasks router (static before dynamic).

---

# PART 2 — 2-HOUR LECTURE PLAN (guided build)

| Time | Segment | Action |
|------|---------|--------|
| 0–15 | Rapid revision | Walk the Part 1 table; cold-call one-line definitions. Show the build map. |
| 15–35 | Scaffold + config + db | Create the package, `config.py`, `database.py`. |
| 35–55 | Models + auth | `models.py` (User/Task + In/Out), `auth.py` (hash, JWT, `get_current_user`). |
| 55–80 | Auth routes | `routers/auth_routes.py`: register (hash), login (JWT). Test in `/docs`. |
| 80–100 | Tasks CRUD (per-user) | `routers/tasks.py`: create/list/get/update/delete, filtered by current user. |
| 100–110 | Run + assignment | Full run via `fastapi dev`; register→login→manage tasks; brief assignment. |
| 110–120 | Module wrap | Celebrate finishing FastAPI; preview Module 3 (LangGraph/agents), which wraps in FastAPI. |

**Tip:** if time is short, build auth + one CRUD route live and leave the rest for the assignment. The must-show payoff: register a user, log in, create a task, and prove another user can't see it.

---

# PART 3 — CODE FILES (`code/taskmanager/` package)
A complete structured project:
```
taskmanager/
├── __init__.py
├── main.py            # app + include_router + startup create_all
├── config.py          # .env settings
├── database.py        # engine + get_session
├── models.py          # User, Task (table) + Create/Public models
├── auth.py            # hashing, JWT, get_current_user dependency
├── routers/
│   ├── __init__.py
│   ├── auth_routes.py # /register, /login
│   └── tasks.py       # /tasks CRUD, per-user
└── .env.example
```
Plus `assignments/solutions.py` — a **single-file** runnable version of the whole app (handy reference).

**Install:** `pip install "fastapi[standard]" sqlmodel pyjwt "passlib[bcrypt]" pydantic-settings`
**Run (from `code/`):** copy `.env.example` → `.env`, then `fastapi dev taskmanager/main.py` → `/docs`.

---

# PART 4 — STUDENT HANDOUT (recap)
- You can now build a **secure, persistent, structured REST API**: routers + `.env` config, SQLModel DB, JWT auth with hashed passwords, per-user CRUD, `response_model`, correct status codes and `HTTPException`.
- **Task Manager** ties it together: register → login (JWT) → manage your own tasks, all persisted, all validated.
- Reuse this project as a **template** for the capstone.
- Homework: extend the Task Manager (due dates, filtering by status, priorities). Push to `batch5-day22-taskmanager` with a README.
- **Next (Module 3, Day 23): LangGraph & Agents** — we start building AI. First stop: LLMs and the Gemini API. Your FastAPI skills will wrap the agents you build.
