# 03_returning_data.py
# -----------------------------------------------------------
# GOAL: Whatever a route returns, FastAPI serializes to JSON - including
# Pydantic models (the direct payoff of Day 12).
#
# RUN:  fastapi dev 03_returning_data.py
#       then open http://127.0.0.1:8000/docs
# -----------------------------------------------------------

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ---- Python built-ins become JSON automatically ----
@app.get("/dict")
def get_dict():
    return {"name": "Ayesha", "age": 25}       # -> JSON object


@app.get("/list")
def get_list():
    return [1, 2, 3, 4]                          # -> JSON array


@app.get("/text")
def get_text():
    return "just a string"                       # -> JSON string


@app.get("/bool")
def get_bool():
    return True                                  # -> true


# ---- Pydantic models become JSON too (FastAPI calls model_dump for you) ----
class Product(BaseModel):
    name: str
    price: float
    in_stock: bool = True


@app.get("/product")
def get_product():
    # Return a Pydantic MODEL object - FastAPI serializes it to JSON.
    return Product(name="Notebook", price=120.0)


@app.get("/products")
def get_products():
    # Even a list of models works.
    return [
        Product(name="Pen", price=50),
        Product(name="Bag", price=800, in_stock=False),
    ]


# KEY TAKEAWAY: you build normal Python objects/models and return them;
# FastAPI handles turning them into a proper JSON HTTP response.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
