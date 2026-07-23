# 02_body_validation.py
# -----------------------------------------------------------
# GOAL: All of Day 12's Pydantic validation applies to the request body.
# Bad data -> automatic 422 response with a precise, field-by-field error.
#
# RUN:  fastapi dev 02_body_validation.py
# TEST: /docs -> POST /products -> "Try it out". Try these bodies:
#   {"name":"Pen","price":50}          -> OK (201)
#   {"name":"P","price":50}            -> 422 (name too short)
#   {"name":"Pen","price":-5}          -> 422 (price must be > 0)
#   {"name":"Pen","price":"abc"}       -> 422 (price not a number)
#   {"price":50}                       -> 422 (name required)
# -----------------------------------------------------------

from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)                 # must be > 0
    quantity: int = Field(default=0, ge=0)     # optional, >= 0
    category: str = "general"

    # Custom rule (Day 12): category must be one of a known set.
    @field_validator("category")
    @classmethod
    def known_category(cls, value):
        allowed = {"general", "stationery", "electronics", "food"}
        if value not in allowed:
            raise ValueError(f"category must be one of {allowed}")
        return value


# In-memory store (a real database comes on Day 18).
PRODUCTS: list[Product] = []


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    # We only reach here if the body PASSED validation.
    PRODUCTS.append(product)
    return {"created": product, "total_products": len(PRODUCTS)}


@app.get("/products")
def list_products():
    return PRODUCTS


# KEY POINT: the 422 you get on bad input is the SAME Pydantic ValidationError
# from Day 12 - now delivered to the client over HTTP. You wrote a model;
# FastAPI turned it into request parsing + validation + error responses + docs.

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
