# 02_first_model.py
# -----------------------------------------------------------
# GOAL: Define your first Pydantic model. A model is a CLASS that inherits
# from BaseModel and describes the shape of your data with type hints.
#
# SETUP:  pip install pydantic
# RUN:    python 02_first_model.py
# -----------------------------------------------------------

from pydantic import BaseModel


# A Pydantic model is just a class inheriting from BaseModel (OOP Day 6!).
class User(BaseModel):
    name: str                   # required, must be a string
    age: int                    # required, must be an integer
    is_active: bool = True       # OPTIONAL: has a default, so it can be omitted


# Notice: we did NOT write __init__ - Pydantic generates it from the fields.
# We pass fields by name, just like keyword arguments.
u1 = User(name="Ayesha", age=25)
print("u1.name:", u1.name)          # Ayesha
print("u1.age:", u1.age)            # 25
print("u1.is_active:", u1.is_active)  # True (used the default)

# Provide the optional field too:
u2 = User(name="Bilal", age=30, is_active=False)
print("\nu2:", u2)                  # Pydantic gives a nice default __repr__

# Fields are just attributes - read them with dot notation.
print("\nu2.is_active:", u2.is_active)

# RECAP of the connections to OOP:
#   - It's a class that INHERITS from BaseModel      (Day 6)
#   - __init__ is auto-generated for us              (Day 3)
#   - fields are attributes accessed with a dot      (Day 2)
# The NEW part: Pydantic validates the data automatically. See file 03.
print("\nA field with a default = optional. A field without one = required.")
