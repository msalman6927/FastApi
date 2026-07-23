# 04_docs_metadata.py
# -----------------------------------------------------------
# GOAL: Make the AUTO DOCS richer. FastAPI builds /docs from your code;
# you can add a title, description, tags, and per-route summaries.
#
# RUN:  fastapi dev 04_docs_metadata.py
#       then open http://127.0.0.1:8000/docs  and compare to /redoc
# -----------------------------------------------------------

from fastapi import FastAPI

# You can describe the whole API here - this shows at the top of /docs.
app = FastAPI(
    title="Batch 5 Demo API",
    description="A tiny API to explore FastAPI's automatic documentation.",
    version="1.0.0",
)


# `tags` group endpoints in the docs; `summary` is the short label shown.
@app.get("/", tags=["general"], summary="Welcome message")
def root():
    """This docstring becomes the endpoint's DESCRIPTION in the docs."""
    return {"message": "Welcome to the Batch 5 Demo API"}


@app.get("/students", tags=["students"], summary="List all students")
def list_students():
    """Returns a hard-coded list of students (a real DB comes on Day 18)."""
    return ["Ayesha", "Bilal", "Chetan"]


@app.get("/students/count", tags=["students"], summary="Count students")
def count_students():
    return {"count": 3}


@app.get("/courses", tags=["courses"], summary="List courses")
def list_courses():
    return ["OOP", "FastAPI", "LangGraph", "RAG"]


# Open /docs: notice endpoints grouped under "general", "students", "courses",
# each with your summary and description. This documentation is generated
# automatically from the code above - always in sync, zero extra effort.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
