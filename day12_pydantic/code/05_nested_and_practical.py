# 05_nested_and_practical.py
# -----------------------------------------------------------
# GOAL: Real data is nested. Use models inside models and lists, then
# SERIALIZE back to dict/JSON. This is the full loop FastAPI runs for you:
#   JSON in -> validate -> typed object -> JSON out.
#
# RUN:  python 05_nested_and_practical.py
# -----------------------------------------------------------

from pydantic import BaseModel, Field
from typing import Optional


# A small model used as a field type inside another model.
class Address(BaseModel):
    city: str
    zip_code: str


class Order(BaseModel):
    item: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class Customer(BaseModel):
    name: str
    email: str
    address: Address                 # NESTED model
    orders: list[Order] = []         # a LIST of models
    notes: Optional[str] = None


# ---- Build from nested Python data (like a parsed JSON body) ----
raw = {
    "name": "Ayesha",
    "email": "ayesha@mail.com",
    "address": {"city": "Karachi", "zip_code": "74000"},
    "orders": [
        {"item": "Book", "quantity": 2, "price": 500},
        {"item": "Pen", "quantity": 5, "price": 50},
    ],
}

# model_validate() validates a whole dict (nested parts included).
customer = Customer.model_validate(raw)

# Nested pieces become real typed objects:
print("City:", customer.address.city)               # Karachi (Address object)
print("First order item:", customer.orders[0].item) # Book (Order object)
print("Number of orders:", len(customer.orders))
print("-" * 50)


# ---- SERIALIZE back out ----
# model_dump() -> Python dict
as_dict = customer.model_dump()
print("model_dump() (Python dict):")
print(" ", as_dict)

# model_dump_json() -> JSON string (what an API would send back)
print("\nmodel_dump_json() (JSON string):")
print(" ", customer.model_dump_json(indent=2))
print("-" * 50)


# ---- Validation works through the WHOLE tree ----
from pydantic import ValidationError
bad = {
    "name": "Bilal",
    "email": "bilal@mail.com",
    "address": {"city": "Lahore"},          # missing zip_code!
    "orders": [{"item": "Bag", "quantity": 0, "price": 800}],  # quantity must be > 0
}
print("Validating bad nested data:")
try:
    Customer.model_validate(bad)
except ValidationError as e:
    for err in e.errors():
        # 'loc' shows the PATH to the problem, e.g. ('address', 'zip_code')
        print(f"  at {err['loc']}: {err['msg']}")

print("\nJSON -> validate -> object -> JSON. This is EXACTLY what FastAPI does.")
