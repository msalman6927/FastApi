# solutions.py  (Instructor solution reference for Day 13 assignment)
# -----------------------------------------------------------
# A single FastAPI app containing all four tasks.
#
# SETUP:  pip install "fastapi[standard]"
# RUN:    fastapi dev solutions.py
# DOCS:   http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

# TASK 2: title + version on the app
app = FastAPI(title="Batch 5 - Day 13 Solution API", version="1.0.0")


# ===========================================================
# TASK 1 (Easy) — Hello API
# ===========================================================
@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/ping")
def ping():
    return {"ping": "pong"}


# ===========================================================
# TASK 2 — About route with metadata
# ===========================================================
@app.get("/about", tags=["info"], summary="About this API")
def about():
    return {
        "author": "Muhammad Salman",
        "course": "Agentic AI - Batch 5",
        "day": 13,
    }


# ===========================================================
# TASK 3 (Medium) — Return Pydantic models
# ===========================================================
class Course(BaseModel):
    id: int
    name: str
    duration_weeks: int


COURSES = [
    Course(id=1, name="OOP", duration_weeks=2),
    Course(id=2, name="FastAPI", duration_weeks=3),
    Course(id=3, name="LangGraph", duration_weeks=3),
]


@app.get("/courses", tags=["courses"], summary="List all courses")
def list_courses():
    return COURSES


@app.get("/courses/count", tags=["courses"], summary="Count courses")
def count_courses():
    return {"count": len(COURSES)}


# ===========================================================
# TASK 4 (Challenge) — Mini Task Manager (read-only)
# ===========================================================
class Task(BaseModel):
    id: int
    title: str
    done: bool = False


TASKS = [
    Task(id=1, title="Learn HTTP", done=True),
    Task(id=2, title="Learn Pydantic", done=True),
    Task(id=3, title="Build first API", done=False),
    Task(id=4, title="Add routes", done=False),
    Task(id=5, title="Explore /docs", done=False),
]


@app.get("/tasks", tags=["tasks"], summary="All tasks")
def all_tasks():
    return TASKS


@app.get("/tasks/pending", tags=["tasks"], summary="Pending tasks")
def pending_tasks():
    return [t for t in TASKS if not t.done]


@app.get("/tasks/completed", tags=["tasks"], summary="Completed tasks")
def completed_tasks():
    return [t for t in TASKS if t.done]


@app.get("/tasks/stats", tags=["tasks"], summary="Task statistics")
def task_stats():
    done = sum(1 for t in TASKS if t.done)
    return {"total": len(TASKS), "done": done, "pending": len(TASKS) - done}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
