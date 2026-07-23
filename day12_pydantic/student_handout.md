# Day 12 Handout — Pydantic (Keep This!)

## What Pydantic does
You **declare the shape** of your data as a class; Pydantic **validates** it, **converts** compatible types, raises **clear errors**, and gives you a typed object. It replaces dozens of hand-written `if` checks. FastAPI (tomorrow) uses it for every request.

## A model is just a class (OOP!)
```python
from pydantic import BaseModel

class User(BaseModel):        # inherits from BaseModel (Day 6)
    name: str                 # required
    age: int                  # required
    is_active: bool = True    # optional (has a default)

u = User(name="Ayesha", age=25)   # no __init__ needed - auto-generated
```
- Field **without** a default = **required**. **With** a default = **optional**.
- `Optional[str] = None` (or `str | None = None`) = optional AND nullable. (Just `Optional[str]` is still required!)

## Coercion & errors
```python
User(name="A", age="25")     # "25" -> 25  (auto-converted)
User(name="A", age="banana") # raises ValidationError (can't convert)
```
Wrap risky construction in `try/except ValidationError`. Inspect with `e.errors()`.
> This ValidationError is what FastAPI returns as a **422** on bad requests.

## Constraints with Field()
```python
from pydantic import Field
age: int = Field(gt=0, lt=150)              # gt/ge/lt/le
name: str = Field(min_length=3, max_length=20)
```

## Custom validators
```python
from pydantic import field_validator

@field_validator("password")
@classmethod
def strong(cls, value):
    if len(value) < 8:
        raise ValueError("too short")   # raise to reject
    return value                        # RETURN to accept (don't forget!)
```

## Nested models & serialization
```python
class Address(BaseModel):
    city: str
class User(BaseModel):
    name: str
    address: Address              # nested model
    hobbies: list[str] = []       # list of values

u.model_dump()        # -> Python dict
u.model_dump_json()   # -> JSON string
User.model_validate(some_dict)   # build/validate from a dict
```
The full loop: **JSON in → validate → typed object → JSON out** = what FastAPI does.

## Pydantic v2 vs v1 (avoid old-tutorial confusion)
| v1 (old) | v2 (we use) |
|----------|-------------|
| `@validator` | `@field_validator` + `@classmethod` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `.parse_obj()` | `.model_validate()` |

## Top mistakes
- `Optional[str]` without `= None` → still required.
- Forgetting `return value` in a validator → field becomes `None`.
- Forgetting `@classmethod` on a validator.
- Using v1 syntax on v2.

## Your homework
`day12_solution.py`: `Book`, `Product` (constraints), `Account` (validators), `Recipe` (nested + serialization). Push to repo `batch5-day12`.

## Next class (Day 13)
**FastAPI — your first API!** We install FastAPI + uvicorn, run a live server on your laptop, and use these Pydantic models as request bodies. Everything from Days 11–12 comes together.
