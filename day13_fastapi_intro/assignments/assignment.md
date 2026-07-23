# Day 13 Assignment — Your First FastAPI App

**Module 02 · Day 13**
**Goal:** Build and run your own FastAPI app with multiple routes, return JSON (including Pydantic models), and use the automatic docs.

> Reminder: activate your `.venv`. `pip install "fastapi[standard]"`. Run with `fastapi dev your_file.py`, then open `http://127.0.0.1:8000/docs`. Stop with Ctrl+C.

---

## Task 1 (Easy) — Hello API
1. Create `app.py` with a FastAPI app.
2. Add a `GET /` route returning `{"message": "Welcome to my API"}`.
3. Add a `GET /ping` route returning `{"ping": "pong"}`.
4. Run it, open `/`, `/ping`, and `/docs` in the browser. Confirm both work.

**Expected:** JSON at both routes; both endpoints visible and testable in `/docs`.

---

## Task 2 (Easy–Medium) — More routes + metadata
1. Add a `GET /about` route returning a dict with your name, the course name, and today's day number (13).
2. Give the app a `title` and `version` in `FastAPI(...)`.
3. Add `tags=["info"]` and a `summary=...` to the `/about` route.
4. Confirm in `/docs` that the endpoint is grouped under "info" with your summary.

**Expected:** `/docs` shows your app title/version and the `/about` endpoint under an "info" group.

---

## Task 3 (Medium) — Return Pydantic models
1. Define a Pydantic model `Course` with fields `id: int`, `name: str`, `duration_weeks: int`.
2. Create an in-memory list of at least 3 `Course` objects.
3. Add `GET /courses` returning the whole list.
4. Add `GET /courses/count` returning `{"count": <number>}`.
5. Verify the JSON output in the browser and in `/docs`.

**Expected output at `/courses` (example):**
```json
[
  {"id": 1, "name": "OOP", "duration_weeks": 2},
  {"id": 2, "name": "FastAPI", "duration_weeks": 3}
]
```

---

## Task 4 (Challenge) — A mini "Task Manager" (read-only for now)
1. Define a model `Task` with `id: int`, `title: str`, `done: bool = False`.
2. Keep an in-memory list of 4–5 `Task`s.
3. Add these GET routes (all read-only — we add create/update/delete on Days 15–17):
   - `GET /tasks` — all tasks.
   - `GET /tasks/pending` — only tasks where `done is False`.
   - `GET /tasks/completed` — only tasks where `done is True`.
   - `GET /tasks/stats` — `{"total": X, "done": Y, "pending": Z}`.
4. Test each route in `/docs` using "Try it out".

**Expected output at `/tasks/stats` (example):**
```json
{"total": 5, "done": 2, "pending": 3}
```

> Hint: use list comprehensions to filter, e.g. `[t for t in TASKS if not t.done]`.

---

## Submission
Put your app in `app.py` (Task 4 can be in the same file or a separate `task_api.py`), commit to repo `batch5-day13`, push to GitHub, and submit the link. Add a short `README.md` saying how to install and run it (`pip install "fastapi[standard]"`, `fastapi dev app.py`).

## Grading checklist
- [ ] App runs with `fastapi dev` and serves JSON
- [ ] Multiple routes with correct paths and methods
- [ ] App has title/version; at least one route has tags + summary
- [ ] Returns Pydantic models serialized to JSON
- [ ] Task 4 filter routes return correct subsets
- [ ] Repo has a `README.md` with run instructions
