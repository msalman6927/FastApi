# Day 19 — Async & Dependencies (`async/await`, `Depends`)

**Module:** 02 — FastAPI | **Duration:** 2 hours
**Prerequisite:** Days 13–18; OOP Day 9 (composition/dependency injection)

> Where we are: You've used `Depends(get_session)` and seen `async def` in tutorials without a full explanation. Today we close both gaps. **Async** lets your API handle many slow I/O operations (database, external APIs, **LLM calls**) efficiently — critical when we build agents later. **Dependencies** (`Depends`) let you share and reuse logic (auth checks, DB sessions, common params) cleanly — the dependency injection idea from OOP Day 9, now a first-class FastAPI feature.
>
> **Instructor note:** Both topics are conceptual. Keep async intuitive (blocking vs non-blocking); don't drown students in event-loop theory. Dependencies are the more immediately useful skill — spend more time there.

---

# PART 1 — INSTRUCTOR DEEP-DIVE

## PART A — ASYNC

## 1.1 The problem async solves
Most API work is **waiting on I/O**: querying a database, calling another API, or (soon) waiting for an **LLM** to respond. During that wait, a normal ("synchronous") function **blocks** — the worker sits idle, unable to handle other requests. With many users, this is slow.

**Async** lets the server, while one request is *waiting* on I/O, **switch to handle other requests**, then come back when the wait is done. Same worker, far more throughput — *for I/O-bound work*.

**Analogy:** a waiter (one worker) taking orders. Synchronous = takes your order, stands frozen at the kitchen until your food is ready, ignoring everyone. Async = takes your order, hands it to the kitchen, and *serves other tables while your food cooks*, returning when it's ready. Async = a smart waiter who doesn't waste waiting time.

## 1.2 `async def` and `await`
```python
import asyncio

@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)      # "await" = pause HERE without blocking others
    return {"done": True}
```
- Mark the function `async def`.
- Use `await` before a call that supports it (async DB drivers, `httpx.AsyncClient`, LLM SDKs' async methods). `await` says "pause here, let others run, resume when ready."
- You can only `await` inside an `async def`.

## 1.3 The golden rule (the one mistake to avoid)
**Never call a blocking function inside `async def`.** `time.sleep(2)` or a synchronous HTTP/DB call inside `async def` freezes the whole event loop — worse than sync. Rules of thumb:
- Use `async def` **only** when you `await` something async inside it.
- If your route calls **blocking** libraries (like the synchronous `requests`, or sync SQLModel), use a **plain `def`** — FastAPI runs it safely in a threadpool so it doesn't block others.
- **Plain `def` is always safe.** When unsure, use `def`. Reach for `async def` when you have genuinely async I/O to await (this becomes important when calling LLMs in Module 3).

## 1.4 Why students should care now
When we build agents (LangGraph) and RAG, we'll call LLMs and vector stores — I/O that can take seconds. Async lets one server handle many such calls concurrently. Today plants the seed; you'll feel the payoff later.

## PART B — DEPENDENCIES

## 1.5 What is a dependency?
A **dependency** is a function (or callable) whose result FastAPI **injects** into your route. You declare `param = Depends(some_function)`, and FastAPI **calls `some_function` for you** and passes its return value in. This is **dependency injection** — the "pass in what you need" idea from OOP Day 9, built into the framework.

```python
from fastapi import Depends

def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items")
def list_items(page: dict = Depends(pagination)):
    return page       # FastAPI ran pagination() using the request's query params
```
`pagination` reads `skip`/`limit` from the query string (FastAPI wires that up), and every route that needs paging just declares `Depends(pagination)` — **write once, reuse everywhere**.

## 1.6 Why dependencies matter (the value)
- **Reuse / DRY:** shared logic (paging, filtering, the DB session, an API-key check) written once, used by many routes.
- **Separation of concerns:** the route focuses on its job; cross-cutting concerns live in dependencies.
- **Testability:** dependencies can be swapped/overridden in tests.
- **Composability:** dependencies can depend on other dependencies (sub-dependencies), building complex behavior from simple pieces.

You already used one: `get_session` (Day 18) is a dependency that yields a DB session.

## 1.7 `yield` dependencies (setup/teardown)
A dependency can `yield` a value and run cleanup afterward — perfect for resources like DB sessions or connections:
```python
def get_session():
    with Session(engine) as session:
        yield session          # provided to the route
    # code after yield runs AFTER the response (cleanup) - here the `with` closes it
```
Everything before `yield` is setup; the yielded value is injected; code after `yield` runs on the way out. This is how you guarantee resources are released.

## 1.8 Dependencies with parameters / classes
A dependency can itself take parameters (query params, other dependencies) — FastAPI resolves the whole chain. Classes can be dependencies too (their `__init__` params become request inputs). And dependencies are great for **auth**: a `get_current_user`/`verify_api_key` dependency runs before the route and can `raise HTTPException(401)` to block unauthorized requests (we build this tomorrow, Day 20).

```python
def verify_key(x_api_key: str = Header(...)):
    if x_api_key != "secret123":
        raise HTTPException(401, "Invalid API key")
    return x_api_key

@app.get("/secure", dependencies=[Depends(verify_key)])
def secure(): ...
```

## 1.9 Common mistakes
1. `async def` with a blocking call inside (freezes the loop) — use `def` for blocking libs.
2. `await`ing something that isn't awaitable → error. Only `await` async calls.
3. Overusing `async` "for speed" — it doesn't speed up CPU work, only concurrent I/O waiting.
4. Repeating the same param logic in every route instead of a shared `Depends`.
5. Forgetting a `yield` dependency's cleanup runs *after* the response.
6. Putting business logic in dependencies that belongs in the route (keep dependencies focused on cross-cutting concerns).

## 1.10 Tricky questions
- **"`async def` or `def`?"** `def` unless you're awaiting genuinely async I/O. Both work; `def` is always safe. Async shines for concurrent I/O (LLMs, async DBs).
- **"Is async multithreading?"** No — it's a single thread cooperatively switching tasks at `await` points. Different model, lighter than threads.
- **"What exactly does `Depends` do?"** It tells FastAPI: "before running my route, call this function (resolving *its* inputs too) and inject the result." It's injection + reuse.
- **"When do I use dependencies?"** DB sessions, auth, shared query params/pagination, rate limits — anything multiple routes need.
- **"Connection to OOP?"** Same principle as Day 9's dependency injection: the route declares what it needs; FastAPI supplies it.

---

# PART 2 — 2-HOUR LECTURE PLAN

| Time | Segment | Action |
|------|---------|--------|
| 0–10 | Recap + hook | The `Depends(get_session)` from Day 18 — "what is that, really?" + why async matters for LLMs. |
| 10–35 | Async (live) | `code/01_async_basics.py`: `async def`, `await asyncio.sleep`, the blocking-call warning. |
| 35–45 | When async vs def | The golden rule; `def` for blocking libs. Keep it practical. |
| 45–80 | Dependencies (live) | `code/02_dependencies.py`: shared pagination dep, reuse across routes, sub-dependencies. |
| 80–100 | Practical DI | `code/03_di_practical.py`: a `verify_key` auth dependency + `yield` resource dependency. |
| 100–112 | Assignment brief | Walk through assignment. |
| 112–120 | Q&A / buffer | Preview Day 20 (auth builds on the dependency you just wrote). |

**Tip:** dependencies are the higher-value half — the shared-pagination demo (45–80) shows immediate DRY payoff. For async, the key takeaway is the *rule* (def unless awaiting async), not deep theory.

---

# PART 3 — CODE FILES (`code/`)
1. `01_async_basics.py` — `async def` + `await`; the blocking-call warning; async external call with `httpx`.
2. `02_dependencies.py` — a reusable pagination dependency; sub-dependencies.
3. `03_di_practical.py` — an API-key `verify_key` dependency and a `yield` resource dependency.

**Install:** `pip install "fastapi[standard]" httpx`
**Run:** `fastapi dev 02_dependencies.py` → `/docs`.

---

# PART 4 — STUDENT HANDOUT (recap)
- **Async** lets one server handle many **I/O waits** (DB, APIs, LLMs) concurrently. `async def` + `await` an async call. **Golden rule:** use plain `def` unless you're awaiting genuinely async I/O — never put a blocking call in `async def`.
- **Dependency** = a function FastAPI calls and **injects** via `param = Depends(func)`. Great for reuse (DB session, pagination, auth). It's OOP Day 9's dependency injection, built in.
- **`yield` dependencies** do setup → yield value → cleanup after the response (e.g., DB sessions).
- Dependencies can guard routes: `raise HTTPException(401)` to block.
- Homework: write shared dependencies and an async route. Push to `batch5-day19`.
- **Next (Day 20):** authentication — API keys / JWT, built on dependencies.
