# Day 18 — Databases (SQLite + SQLModel, connected to FastAPI)

**Module:** 02 — FastAPI | **Duration:** 2 hours
**Prerequisite:** Days 12–17 (Pydantic, CRUD), OOP (classes)

> Where we are: Yesterday's API loses all data when the server restarts (it's in RAM). Real apps need **persistence** — data that survives restarts and can grow to millions of rows. That's a **database**. Today we connect a real database (SQLite) to FastAPI using **SQLModel** — a library that combines Pydantic (which you know) with SQLAlchemy (the standard Python ORM). Your CRUD API becomes permanent.
>
> **Instructor note:** SQLModel is by the creator of FastAPI and is literally **SQLAlchemy + Pydantic** underneath. Because students already know Pydantic models, a database table looks almost identical (just `table=True`). This is the gentlest possible on-ramp to databases. If students find SQLAlchemy tutorials online, tell them SQLModel *is* SQLAlchemy with a Pydantic-friendly face.

---

# PART 1 — INSTRUCTOR DEEP-DIVE

## 1.1 What is a database and why?
A **database** stores data permanently and lets you query it efficiently. Compared to our in-memory dict:
- **Persistent** — survives restarts and crashes (data on disk, not RAM).
- **Scalable** — handles huge datasets and concurrent users.
- **Queryable** — filter/sort/join with a powerful query language.
- **Safe** — transactions keep data consistent.

We use a **relational (SQL) database**: data lives in **tables** (like spreadsheets) with rows (records) and columns (fields). Each row has a unique **primary key** (usually an auto-incrementing `id`). *(NoSQL databases like MongoDB store documents instead; we stick with SQL — it's the default for structured app data.)*

## 1.2 Why SQLite?
**SQLite** is a database that lives in a **single file** (e.g., `app.db`) with **zero setup** — no server to install or run. It's built into Python. Perfect for learning and small apps. Later (deployment module) you can swap to PostgreSQL by changing one connection string — the code stays the same thanks to the ORM.

## 1.3 What is an ORM? (the key concept)
Normally you talk to a SQL database by writing **SQL** strings (`SELECT * FROM users WHERE id = 5`). An **ORM (Object-Relational Mapper)** lets you work with **Python objects and classes instead of raw SQL**. You define a class; the ORM maps it to a table; you call Python methods; the ORM writes the SQL for you.
- **Class ↔ Table**, **object ↔ row**, **attribute ↔ column**.
- You write `session.add(user)` instead of `INSERT INTO ...`.

This is a perfect fit for our OOP + Pydantic background: a database table is just a class.

## 1.4 SQLModel = Pydantic + SQLAlchemy
A SQLModel table model looks like a Pydantic model with two additions: `table=True` and a primary-key field.
```python
from sqlmodel import SQLModel, Field

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # auto-increment PK
    name: str
    power: str
    age: int | None = None
```
- `table=True` tells SQLModel this maps to a **database table**.
- `id: int | None = Field(default=None, primary_key=True)` — the primary key; `None` before insert, the DB assigns it on save.
- Other fields are columns, typed like Pydantic.

## 1.5 Engine & Session (how you talk to the DB)
Two objects to understand:
- **Engine** — the connection to the database file. Created once for the whole app: `create_engine("sqlite:///app.db")`.
- **Session** — a short-lived workspace for a set of operations (add/query/commit). You open one per request, do your work, commit, close.

```python
from sqlmodel import create_engine, Session, SQLModel

engine = create_engine("sqlite:///app.db")
SQLModel.metadata.create_all(engine)   # creates tables from your models (once)

with Session(engine) as session:
    session.add(Hero(name="Deadpond", power="regen"))
    session.commit()                    # save to disk
```
- `create_all(engine)` creates any missing tables based on your `table=True` models.
- `session.add(obj)` stages an insert; `session.commit()` writes it.
- Query with `session.get(Hero, id)` (by primary key) or `session.exec(select(Hero))` (general queries).

## 1.6 Connecting to FastAPI (the session dependency)
Each request should get its own session. FastAPI's **dependency injection** (`Depends`, formalized tomorrow) makes this clean:
```python
from fastapi import Depends
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session          # provide a session, auto-close after the request

@app.post("/heroes")
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)      # reload to get the DB-assigned id
    return hero
```
- `Depends(get_session)` gives each endpoint a fresh session, automatically closed afterward. (This *is* dependency injection — the pattern from OOP Day 9, now doing real work. Full treatment tomorrow.)
- `session.refresh(hero)` fetches the new `id` the database generated.

## 1.7 CRUD with a database (the operations)
- **Create:** `session.add(obj)` → `commit()` → `refresh(obj)`.
- **Read all:** `session.exec(select(Model)).all()`.
- **Read one:** `session.get(Model, id)` (returns `None` if missing → 404).
- **Update:** get it, set attributes, `add` + `commit` + `refresh`.
- **Delete:** get it, `session.delete(obj)` → `commit()`.

Same CRUD shape as Day 17 — only the storage changed from a dict to a real DB. That's the payoff of yesterday's structure.

## 1.8 Separate table model vs API models (good practice)
Best practice mirrors Day 16–17: a `HeroCreate` (input, no id), `HeroPublic` (output, with id), and the `Hero` **table** model. This keeps the DB schema separate from what clients send/receive. For today's teaching we can start with one table model and introduce the split in the practical example — don't overwhelm on the first DB day.

## 1.9 Common mistakes
1. **Forgetting `commit()`** → changes never save.
2. **Forgetting `refresh()`** → the returned object has `id=None`.
3. **Not calling `create_all`** → "no such table" error.
4. **Sharing one global session** across requests → concurrency bugs. Use the per-request dependency.
5. **`echo=True` left on in production** — fine for learning (prints SQL), noisy for prod.
6. **SQLite + threads:** pass `connect_args={"check_same_thread": False}` for SQLite with FastAPI (shown in code). 
7. Deleting the `.db` file to "reset" — fine in dev, but understand you're wiping data.

## 1.10 Tricky questions
- **"SQL vs NoSQL?"** SQL = structured tables + relationships (our choice, default for app data). NoSQL = flexible documents (MongoDB). We use SQL.
- **"Where's the data stored?"** In the `app.db` file on disk. Delete it and the data's gone; back it up like any file.
- **"Do I write SQL?"** Rarely, thanks to the ORM — but knowing basic SQL helps for debugging. The ORM generates it for you.
- **"How do I move to PostgreSQL later?"** Change the connection string (`postgresql://...`) and install a driver; your models/queries stay the same.
- **"Is SQLModel production-ready?"** Yes for many apps; SQLAlchemy (its base) powers huge systems.

---

# PART 2 — 2-HOUR LECTURE PLAN

| Time | Segment | Action |
|------|---------|--------|
| 0–10 | Recap + hook | Restart yesterday's API → data gone. "Let's make it permanent." Install `pip install sqlmodel`. |
| 10–35 | DB basics (live, no API) | `code/01_sqlmodel_basics.py`: define a table model, create engine/tables, insert + query. Open the `.db` file exists. |
| 35–70 | CRUD with DB + FastAPI (live) | `code/02_crud_with_db.py`: session dependency, create/read/update/delete persisted. Test in `/docs`. |
| 70–90 | Persistence proof | Restart the server → data still there! Run `code/03_inspect_db.py` to read the file directly. |
| 90–108 | Input/output models + assignment | Show the Create/Public split; brief assignment. |
| 108–120 | Q&A / buffer | Preview Day 19 (async & dependencies — the `Depends` you just used). |

**Tip:** the unforgettable moment is restarting the server and seeing the data survive (70–90). That single demo justifies the whole lesson. Contrast explicitly with Day 17's in-memory loss.

---

# PART 3 — CODE FILES (`code/`)
1. `01_sqlmodel_basics.py` — define a table, create engine/tables, insert & query (pure script, no API).
2. `02_crud_with_db.py` — full CRUD FastAPI app backed by SQLite via a session dependency.
3. `03_inspect_db.py` — read the database file directly to prove data persisted.

**Install:** `pip install sqlmodel`
**Run API:** `fastapi dev 02_crud_with_db.py` → `/docs`. **Basics/inspect:** `python 01_sqlmodel_basics.py`, `python 03_inspect_db.py`.

---

# PART 4 — STUDENT HANDOUT (recap)
- **Database** = permanent, queryable storage (survives restarts). We use **SQLite** (one file, zero setup).
- **ORM** = work with Python objects instead of raw SQL. **SQLModel = Pydantic + SQLAlchemy**; a table is a model with `table=True` + a primary key.
- **Engine** (one per app, the connection) + **Session** (per request, the workspace). `add` → `commit` → `refresh`.
- Connect to FastAPI with a **session dependency** (`Depends(get_session)`).
- CRUD is the same shape as Day 17 — only storage changed.
- Homework: persist a resource with SQLModel + full CRUD. Push to `batch5-day18`.
- **Next (Day 19):** async & dependencies — what `Depends` really is, and `async def` for I/O.
