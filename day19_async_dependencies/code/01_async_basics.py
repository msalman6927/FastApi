# 01_async_basics.py
# -----------------------------------------------------------
# GOAL: Understand async def / await and the golden rule of when to use it.
#
# SETUP:  pip install "fastapi[standard]" httpx
# RUN:    fastapi dev 01_async_basics.py  ->  /docs
# -----------------------------------------------------------

import asyncio
import httpx
from fastapi import FastAPI

app = FastAPI()


# A plain sync route - always safe. Use this for normal/CPU or blocking work.
@app.get("/sync")
def sync_route():
    return {"type": "sync", "note": "plain def is always safe"}


# An async route: `await` pauses HERE without blocking other requests.
@app.get("/async")
async def async_route():
    await asyncio.sleep(1)          # simulate waiting on I/O (non-blocking)
    return {"type": "async", "waited": "1s without blocking others"}


# Async is BUILT for calling external services (APIs, and later LLMs).
# httpx.AsyncClient lets us await an outgoing HTTP request.
@app.get("/joke")
async def get_joke():
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            "https://official-joke-api.appspot.com/jokes/programming/random")
        joke = r.json()[0]
    return {"setup": joke["setup"], "punchline": joke["punchline"]}


# -----------------------------------------------------------------
# THE GOLDEN RULE:
#   - Use `async def` ONLY when you `await` something async inside.
#   - NEVER put a blocking call (time.sleep, the sync `requests` lib, sync DB)
#     inside `async def` - it freezes the event loop for EVERYONE.
#   - If you must use blocking libraries, use a plain `def` route: FastAPI
#     runs it in a threadpool so it won't block others.
#   - When unsure -> use `def`. Reach for `async def` for real async I/O
#     (this matters a lot when we call LLMs in Module 3).
# -----------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
