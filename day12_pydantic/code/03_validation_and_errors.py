# 03_validation_and_errors.py
# -----------------------------------------------------------
# GOAL: See Pydantic's two superpowers:
#   1) TYPE COERCION - convert compatible types automatically ("25" -> 25)
#   2) VALIDATION ERRORS - a clear, structured error when data is bad
#
# RUN:  python 03_validation_and_errors.py
# -----------------------------------------------------------

from pydantic import BaseModel, ValidationError
from typing import Optional


class User(BaseModel):
    name: str
    age: int
    nickname: Optional[str] = None    # optional AND nullable (note the = None)


# ---- 1) COERCION: a numeric string is converted to int automatically ----
u = User(name="Ayesha", age="25")     # age given as the STRING "25"
print("Coercion: age =", u.age, "| type:", type(u.age).__name__)  # 25, int
print("-" * 50)


# ---- 2) VALIDATION ERROR: impossible conversion is rejected ----
print("Trying age='banana':")
try:
    User(name="Ayesha", age="banana")
except ValidationError as e:
    print(e)                          # names the field + the exact problem
print("-" * 50)


# ---- Missing a REQUIRED field also fails ----
print("Trying to omit required 'age':")
try:
    User(name="Ayesha")
except ValidationError as e:
    print(e)                          # age: Field required
print("-" * 50)


# ---- Inspecting errors programmatically (useful when building APIs) ----
print("errors() as data you can loop over:")
try:
    User(name=123, age="banana")      # BOTH fields wrong
except ValidationError as e:
    for err in e.errors():
        print(f"  field={err['loc']}  problem={err['msg']}")
print("-" * 50)


# ---- Required vs optional vs nullable ----
# name/age  -> required (no default)
# nickname  -> optional AND nullable (Optional[str] = None)
ok = User(name="Bilal", age=40)       # nickname omitted -> None
print("nickname when omitted:", ok.nickname)
print("\nKey point: this ValidationError is what FastAPI returns as a 422 tomorrow!")
