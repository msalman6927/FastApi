# Day 22 Assignment — FastAPI Mini-Project (Extend the Task Manager)

**Module 02 · Day 22 — Portfolio Project**
**Goal:** Extend the structured, authenticated, database-backed Task Manager API. This is your Module 2 portfolio piece.

> Start from the `taskmanager/` package (or the single-file `assignments/solutions.py`). Keep the clean structure.

---

## Task 1 (Core) — Run and verify
1. Get the base project running (`fastapi dev taskmanager/main.py`).
2. In `/docs`: register two users, log in as each, and prove **user A cannot see user B's tasks**.

---

## Task 2 (Medium) — Richer tasks
1. Add fields to `Task`: `priority: int = 3` (1–5) and `due_date: str | None = None`.
2. Update the create/update models and endpoints accordingly.
3. Validate `priority` is between 1 and 5 (Pydantic `Field(ge=1, le=5)`).

---

## Task 3 (Medium) — Filtering & search
1. `GET /tasks?done=true|false` — filter by completion (optional query param).
2. `GET /tasks?q=...` — search in the title.
3. Combine both when provided. (All scoped to the current user.)

---

## Task 4 (Challenge) — Stats + polish
1. `GET /tasks/stats` — return `{"total", "done", "pending"}` for the current user (place before `/tasks/{id}`).
2. Add a `README.md` with: what the app does, setup/run commands, the `.env` keys, and example requests.
3. Ensure `.env` is git-ignored and `.env.example` is committed.

---

## Submission
The `taskmanager/` package → repo `batch5-day22-taskmanager` with a README. This is a strong portfolio project — make it clean.

## Checklist
- [ ] Runs end-to-end; per-user task isolation verified
- [ ] Richer task fields with validation
- [ ] Filtering + search query params (scoped to the user)
- [ ] Stats endpoint (correct route order)
- [ ] README + `.env.example`; `.env` not committed
