 Pydantic (Data Validation & Models)


## 1.1 The problem Pydantic solves

Imagine you receive user data as a dictionary (like a parsed JSON body):
```python
data = {"name": "Ayesha", "age": "twenty", "email": "not-an-email"}
```
Without a tool, *you* must hand-write validation for every field:
```python
if "name" not in data: raise ValueError("name required")
if not isinstance(data["age"], int): raise ValueError("age must be int")
# ...repeat for every field, every endpoint... exhausting and error-prone
```
This is tedious, repetitive, and easy to get wrong — and you'd rewrite it for every API endpoint. **Pydantic replaces all of it**: you *declare* the shape once, and Pydantic validates, converts types, and produces clear errors automatically.

## 1.2 What is Pydantic?

**Pydantic** is a data-validation library. You define a **model** — a class describing what fields exist and their types — and Pydantic:
1. **Validates** incoming data against that model.
2. **Converts (coerces)** compatible types automatically (`"25"` → `25`).
3. **Raises a clear `ValidationError`** listing exactly what's wrong.
4. **Gives you a clean Python object** with typed attributes and editor autocomplete.

The magic: **you describe data with Python type hints, and Pydantic enforces them at runtime.** Normally type hints are just documentation Python ignores; Pydantic makes them *real*.

Install: `uv add pydantic`. We're on **Pydantic v2** (current) — note the syntax if students find v1 tutorials online (see 1.10).

## 1.3 Your first model

```python
from pydantic import BaseModel

class User(BaseModel):          # inherit from BaseModel (OOP Day 6!)
    name: str                   # required, must be a string
    age: int                    # required, must be an int
    is_active: bool = True      # optional, defaults to True

u = User(name="Ayesha", age=25)
print(u.name)        # Ayesha
print(u.age)         # 25
print(u.is_active)   # True
```

Teaching points:
- **It's just a class inheriting from `BaseModel`.** Everything students know about classes applies.
- **No `__init__` needed** — Pydantic generates one from the field declarations. (Connect back: OOP Day 3's `__init__` is written *for you* here.)
- **Fields are declared with type hints** (`name: str`). This is the "annotation" syntax; Pydantic reads it.
- **A field with a default value is optional**; one without a default is **required**.
- Access fields with normal dot notation (`u.name`) — they're just attributes.

## 1.4 Automatic type coercion (and validation failure)

Pydantic tries to **convert** data to the declared type when it's sensible:
```python
u = User(name="Ayesha", age="25")   # age is a STRING "25"...
print(u.age, type(u.age))           # 25 <class 'int'>  -> coerced to int!
```
`"25"` becomes `25` because it's a valid integer string. This is very handy for web data (which often arrives as strings).

But if conversion is impossible, it raises a `ValidationError`:
```python
from pydantic import ValidationError
try:
    User(name="Ayesha", age="banana")   # can't turn "banana" into an int
except ValidationError as e:
    print(e)   # clear message: age -> Input should be a valid integer
```

Key teaching moments:
- The `ValidationError` message is **structured and specific** — it names the field, the problem, and the bad value. This is what makes debugging painless.
- **Missing a required field** also raises `ValidationError` (`Field required`).
- You can inspect errors programmatically with `e.errors()` (returns a list of dicts) — useful when building APIs.
- Note: by default Pydantic v2 is "lax" and coerces; there's a strict mode, but keep it simple today. Just know `"25"→25` works, `"banana"→int` fails.

## 1.5 Optional fields, defaults, and `None`

```python
from typing import Optional

class Product(BaseModel):
    name: str                          # required
    price: float                       # required
    description: Optional[str] = None  # optional, may be missing/None
    in_stock: bool = True              # optional with a default
```
Teach the distinction clearly:
- **Required:** no default (`name: str`). Must be provided or it errors.
- **Optional with default:** has a default (`in_stock: bool = True`). Can be omitted.
- **Optional / nullable:** `Optional[str] = None` (or modern `str | None = None`) means "a string or nothing." Common for fields that may be absent.

Common confusion: `Optional[str]` alone (without `= None`) is still *required* — it just allows `None` as a value. To make it truly optional you also give it a default. Spell this out; it trips people up.
### Optional String with Strict Validation

```python
from pydantic import StrictStr
from typing import Optional

description: Optional[StrictStr] = None
```

**Meaning:**
- `description` can be a string or `None`.
- If a non-string value (e.g. `123`) is provided, validation will fail.
- 
## 1.6 Field constraints with `Field()`

For rules beyond the type (ranges, lengths), use `Field()`:
```python
from pydantic import BaseModel, Field

class Account(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(gt=0, lt=150)          # gt = greater than, lt = less than
    balance: float = Field(default=0, ge=0) # ge = greater-than-or-equal
    email: str = Field(pattern=r".+@.+\..+") # simple regex pattern
```
Common constraints to know:
- Numbers: `gt`, `ge`, `lt`, `le` (>, ≥, <, ≤).
- Strings: `min_length`, `max_length`, `pattern` (regex).
- `default=...` for the default value; `Field(...)` (literal ellipsis) marks required explicitly.
- `Field(description=..., examples=...)` adds documentation that later shows up in FastAPI's auto-generated docs — a nice preview.

This is exactly the validation you hand-wrote with `@property` setters on OOP Day 5 — but declarative and reusable. Make that connection explicit.

## 1.7 Custom validators (`@field_validator`)

When constraints aren't enough, write custom logic with `@field_validator`:
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    password: str

    @field_validator("password")
    @classmethod
    def password_strong(cls, value):
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters")
        if not any(c.isdigit() for c in value):
            raise ValueError("password must contain a digit")
        return value        # ALWAYS return the (possibly cleaned) value
```
- Decorated with `@field_validator("field_name")` and `@classmethod` (it receives `cls`).
- It receives the field's value; **raise `ValueError`** to reject, or **return the value** (optionally transformed, e.g., `value.strip().lower()`) to accept.
- You can validate multiple fields: `@field_validator("field1", "field2")`.
- For rules spanning *multiple* fields (e.g., "password and confirm_password must match"), use `@model_validator(mode="after")` — mention it exists; a light demo is enough.

## 1.8 Serialization: model ↔ dict ↔ JSON

APIs speak JSON, so you need to convert models back to dict/JSON:
```python
u = User(name="Ayesha", age=25)
u.model_dump()          # -> {'name': 'Ayesha', 'age': 25}   (Python dict)
u.model_dump_json()     # -> '{"name":"Ayesha","age":25}'    (JSON string)

# And the reverse - build a model FROM a dict (e.g., parsed JSON):
data = {"name": "Bilal", "age": 30}
u2 = User(**data)                    # unpack dict into fields
u3 = User.model_validate(data)       # or validate a dict directly
```
This is the full loop: JSON in → validate → work with a typed object → `model_dump_json()` → JSON out. **This is precisely what FastAPI does for every request/response**, using your models. (v2 names: `model_dump`/`model_dump_json`; v1 used `.dict()`/`.json()` — see 1.10.)

## 1.9 Nested models & lists

Real data is nested; Pydantic handles it naturally by using models as field types:
```python
class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address                 # a nested model
    hobbies: list[str] = []          # a list of strings
    friends: list["User"] = []       # even a list of models
```
Pydantic validates the whole tree — if `address.city` is missing, you get a precise nested error path (`address -> city`). This mirrors how JSON objects nest (Day 11), and it's how APIs model complex payloads.



# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
