# Day 12 — Pydantic (Data Validation & Models)

**Module:** 02 — FastAPI
**Duration:** 2 hours
**Prerequisite:** OOP module (esp. Day 5 encapsulation/validation, Day 6 inheritance), Day 11 (JSON)

> Where we are: Day 11 you learned APIs exchange **JSON data**. But data from the outside world is *untrusted* — a user might send `age: "banana"` or forget a required field. Before FastAPI can safely accept requests, we need a way to **define the shape of our data and validate it automatically**. That tool is **Pydantic**. It's the single most important prerequisite for FastAPI — FastAPI literally uses Pydantic under the hood to validate every request. Master it today and FastAPI (Day 13) becomes easy.
>
> **Instructor note:** Pydantic connects straight to what students already know. A Pydantic model is a **class** that **inherits** from `BaseModel` (OOP Day 6), and it does automatic **validation** — the professional version of the `@property` setters from OOP Day 5. Lean on those connections; it makes a "new" library feel familiar.

---

# PART 1 — INSTRUCTOR DEEP-DIVE (teach yourself first)

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
Teaching points:
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

## 1.10 Pydantic v1 vs v2 (so students aren't confused by old tutorials)
Many online tutorials use v1. Key renames in **v2 (what we use)**:
| v1 (old) | v2 (current) |
|----------|--------------|
| `@validator` | `@field_validator` (+ `@classmethod`) |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `class Config:` | `model_config = ConfigDict(...)` |
| `.parse_obj()` | `.model_validate()` |
Tell students: if a tutorial uses `.dict()` or `@validator`, it's v1 — translate to the v2 names above.

## 1.11 Common mistakes (warn students)
1. **`Optional[str]` without `= None`** thinking it's optional — it's still *required*, just nullable. Add the default.
2. **Forgetting `return value`** in a `@field_validator` → the field becomes `None`. Always return.
3. **Forgetting `@classmethod`** on a v2 validator → error.
4. **Expecting silent failure** — Pydantic *raises* `ValidationError`; wrap risky construction in try/except when you want to handle it gracefully.
5. **Using v1 syntax** (`.dict()`, `@validator`) on v2 → attribute errors. Use v2 names.
6. **Confusing coercion limits** — `"25"→25` works, but `"twenty"→int` fails. Coercion is for *convertible* values only.
7. **Mutating a model expecting no validation** — by default v2 doesn't re-validate on assignment unless configured; not a beginner concern, just don't rely on it.

## 1.12 Tricky student questions & your answers

**Q: "How is a Pydantic model different from a normal class?"**
A: It's a class that inherits from `BaseModel`. The difference is Pydantic auto-generates `__init__`, and *validates + converts* the data against your type hints at creation. A normal class does none of that automatically.

**Q: "How is this different from a dataclass?"**
A: `@dataclass` bundles data with an auto `__init__` but does **no validation or coercion**. Pydantic adds runtime validation, type conversion, JSON serialization, and rich errors. For untrusted/external data (APIs), use Pydantic.

**Q: "Why do type hints suddenly matter? I thought Python ignored them."**
A: Plain Python does ignore them at runtime. Pydantic *reads* them and enforces them. That's its whole trick — making annotations real.

**Q: "When does validation run?"**
A: When you create the model (`User(...)`) or call `model_validate(...)`. If the data is bad, it raises immediately — you never get a half-valid object.

**Q: "Do I need Pydantic if I'm careful with my data?"**
A: For your own trusted code, maybe not. For data from *outside* (API requests, user input, files), always — you can't trust external data, and Pydantic makes checking it one line instead of fifty.

**Q: "How does this connect to FastAPI?"**
A: In FastAPI you declare a Pydantic model as your request body. FastAPI automatically parses the JSON, validates it against your model, returns a **422** with a clear error if it's bad, and hands your endpoint a clean typed object. Everything today is what FastAPI runs for you.

---

# PART 2 — 2-HOUR LECTURE PLAN (minute-by-minute)

| Time | Segment | What you do |
|------|---------|-------------|
| **0–10 min** | **Recap Day 11 + hook** | Recap: APIs exchange JSON, but external data is untrusted. Show `code/01_without_pydantic.py` — the mess of hand-written validation. "There's a better way." |
| **10–30 min** | **First model (live)** | `code/02_first_model.py`: `class User(BaseModel)`, fields as type hints, no `__init__` needed. Connect to OOP inheritance + auto-constructor. |
| **30–55 min** | **Coercion & errors (live)** | `code/03_validation_and_errors.py`: `"25"→25`, `"banana"`→`ValidationError`, missing required field, `e.errors()`. Required vs optional vs nullable. |
| **55–80 min** | **Constraints & custom validators (live)** | `code/04_field_constraints.py`: `Field(gt=..., min_length=...)`, then `@field_validator` for custom rules. Tie back to OOP Day 5 `@property` validation. |
| **80–100 min** | **Nested models + serialization (live)** | `code/05_nested_and_practical.py`: nested models, lists, `model_dump`/`model_dump_json`, building from a dict. The full JSON→object→JSON loop. |
| **100–112 min** | **Assignment brief + v1/v2 note** | Warn about old tutorials (v1 vs v2). Walk through `assignments/assignment.md`. |
| **112–120 min** | **Q&A / buffer** | Answer questions; preview Day 13 — "tomorrow FastAPI runs all of this for you on real requests." |

**Timing tip:** the highest-impact demo is the `ValidationError` in `03` — show the actual error message and say "this exact error is what your API will return as a 422 tomorrow." Constraints + custom validators (55–80) are the meat; give them room. If short on time, `@model_validator` (cross-field) can be a mention rather than a full demo.

---

# PART 3 — CODE / DEMO FILES (in `code/`, run in this order)

1. `01_without_pydantic.py` — the pain of hand-written validation (motivation).
2. `02_first_model.py` — `BaseModel`, fields as type hints, auto-`__init__`.
3. `03_validation_and_errors.py` — coercion, `ValidationError`, required/optional/nullable.
4. `04_field_constraints.py` — `Field()` constraints + `@field_validator` custom rules.
5. `05_nested_and_practical.py` — nested models, lists, `model_dump`/`model_dump_json`, dict↔model.

**Install command needed today:**
```
pip install pydantic
```
(No internet needed to run the demos — Pydantic is local. `EmailStr` needs the extra `pip install "pydantic[email]"`; we avoid it to keep installs simple and use a regex/validator instead.)

---

# PART 4 — STUDENT HANDOUT
See `student_handout.md` in this folder for the short student recap.
