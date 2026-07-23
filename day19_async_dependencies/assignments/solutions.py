# solutions.py  (Day 19 - async & dependencies)
# SETUP: pip install "fastapi[standard]"
# RUN:   fastapi dev solutions.py  ->  /docs

import asyncio
from fastapi import FastAPI, Depends, Header, HTTPException, status

app = FastAPI(title="Day 19 Solutions")


# ===== Task 1 - async route =====
# GOLDEN RULE: use `async def` only when you `await` genuinely async I/O.
# Use plain `def` for blocking libraries (FastAPI runs def in a threadpool).
@app.get("/wait")
async def wait():
    await asyncio.sleep(1)
    return {"status": "done"}


# ===== Task 2 - shared pagination dependency =====
PRODUCTS = [f"product_{i}" for i in range(1, 31)]
ORDERS = [f"order_{i}" for i in range(1, 31)]


def pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/products")
def list_products(page: dict = Depends(pagination)):
    return PRODUCTS[page["skip"]: page["skip"] + page["limit"]]


@app.get("/orders")
def list_orders(page: dict = Depends(pagination)):
    return ORDERS[page["skip"]: page["skip"] + page["limit"]]


# ===== Task 3 - guard dependency =====
def verify_token(token: str = Header(...)):
    if token != "letmein":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Bad token")
    return token


@app.get("/dashboard")
def dashboard(token: str = Depends(verify_token)):
    return {"dashboard": "welcome", "token": token}


# ===== Task 4 - combine everything =====
def get_db():
    db = ["Buy milk", "Learn FastAPI", "Call mom", "Deploy app", "Sleep"]
    try:
        yield db                      # setup: provide the "database"
    finally:
        print("[db] cleanup after response")   # teardown


def common_params(q: str | None = None, page: dict = Depends(pagination)):
    return {"q": q, **page}           # sub-dependency composition


@app.get("/notes")
def notes(
    token: str = Depends(verify_token),          # protected
    db: list = Depends(get_db),                  # yield dependency
    params: dict = Depends(common_params),       # composed dependency
):
    results = db
    if params["q"]:
        results = [n for n in results if params["q"].lower() in n.lower()]
    start = params["skip"]
    return results[start: start + params["limit"]]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
