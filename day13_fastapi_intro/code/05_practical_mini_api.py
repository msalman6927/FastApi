# 05_practical_mini_api.py
# -----------------------------------------------------------
# GOAL: A small but complete multi-route API that ties the day together:
# a "Quotes" API with several GET endpoints returning JSON.
# (Path parameters and request bodies come on Days 14-15; today is GET + JSON.)
#
# RUN:  fastapi dev 05_practical_mini_api.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

import random
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Quotes API", version="1.0.0")


# A model describing the shape of a quote (Day 12).
class Quote(BaseModel):
    id: int
    text: str
    author: str


# Our "database" for today is just a list in memory (real DB on Day 18).
QUOTES = [
    Quote(id=1, text="Talk is cheap. Show me the code.", author="Linus Torvalds"),
    Quote(id=2, text="Simplicity is the soul of efficiency.", author="Austin Freeman"),
    Quote(id=3, text="First, solve the problem. Then, write the code.", author="John Johnson"),
]


@app.get("/", tags=["general"], summary="API welcome")
def root():
    return {"message": "Welcome to the Quotes API", "total_quotes": len(QUOTES)}


@app.get("/quotes", tags=["quotes"], summary="Get all quotes")
def get_all_quotes():
    # Returning a list of Pydantic models -> JSON array automatically.
    return QUOTES


@app.get("/quotes/random", tags=["quotes"], summary="Get a random quote")
def get_random_quote():
    return random.choice(QUOTES)


@app.get("/quotes/count", tags=["quotes"], summary="How many quotes")
def get_count():
    return {"count": len(QUOTES)}


# NOTE: "/quotes/random" and "/quotes/count" are defined BEFORE any
# "/quotes/{id}" route would be. Route ORDER can matter when paths overlap -
# we'll explore path parameters and that subtlety tomorrow (Day 14).

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
